"""pyguiforms' hand-written layer over the generated 1:1 layer (``_abi``).

It adds the invariants the C ABI leaves to its caller, and nothing else:

- Loading: the one library, ``gui_forms_abi1`` (``libgui_forms_abi.1.dylib``,
  ``libgui_forms_abi.so.1``, ``gui_forms_abi1.dll``), found by
  ``GUI_FORMS_ABI_LIBRARY`` or in ``pyguiforms/_native/`` (a wheel ships it
  there), loaded by absolute path and kept loaded for the process: the
  tables it lends point into it.
- Negotiation: each table is negotiated once, at the pinned manifest's
  version. A slot the library did not serve (past the negotiated
  struct_size, or null) answers GF_STATUS_UNSUPPORTED_VERSION instead of
  calling through null, as gui_forms ``gf_abi.hpp`` does. Each slot is read
  once: ctypes builds a new function object on every field read.
- Failures: a refused call becomes ``GuiFormsError`` with the calling
  thread's error detail. Only the caller knows which statuses it expects,
  so ``check`` is called where a failure is exceptional.
- Callbacks: one module-level trampoline per callback slot type, made at
  import for the process, so lending a callback makes no executable
  closure. A callback's context is a key into ``CallbackRegistry``, issued
  once and never reused; the library's release forgets it. No Python
  exception crosses into the library: the trampoline catches it as a
  ``CallbackFailure``. Under a call that returns into Python the caller's
  ``check`` rethrows it. Under the event loop the rule is close and raise:
  the running window is asked to close and ``run`` raises the failure,
  unless the program's failure hook (``set_failure_hook``) handles it, in
  which case the loop carries on.
- Ownership: ``ObjectReference`` gives its reference back exactly once
  (``release``, the context manager, or the finalizer as a last resort;
  objects.release is callable from any thread). ``Subscription`` ends once.

Threads (gf_abi.h, Threads): the library's UI thread is the thread that
creates the first object, and every table function but objects.retain,
objects.release and dispatch.begin_invoke runs on it alone. pyguiforms makes
the Python main thread that thread (AppKit needs the process's main thread)
and refuses UI calls from other threads with ``WrongThreadError`` before
they reach the library. ctypes releases the GIL around every library call
and takes it in every trampoline. The registry, the schema cache and the
reference release are locked, so a free-threaded build (3.13t and later)
needs nothing more; the library itself calls back on the UI thread only,
never two callbacks at once.
"""

from __future__ import annotations

import ctypes
import os
import pathlib
import sys
import threading
import typing

from pyguiforms import _abi
from pyguiforms import schema
from pyguiforms import values

# ---------------------------------------------------------------- the library


def library_file_name() -> str:
    """The file gui_forms' cmake/CAbi.cmake builds for this platform and ABI major."""
    major: str = str(_abi.ABI_MAJOR)
    if sys.platform == "win32":
        return "gui_forms_abi" + major + ".dll"
    if sys.platform == "darwin":
        return "libgui_forms_abi." + major + ".dylib"
    return "libgui_forms_abi.so." + major


def find_library() -> pathlib.Path:
    """GUI_FORMS_ABI_LIBRARY when set, else the copy a wheel ships in pyguiforms/_native/."""
    configured: str | None = os.environ.get("GUI_FORMS_ABI_LIBRARY")
    if configured is not None and configured != "":
        return pathlib.Path(configured)
    bundled: pathlib.Path = pathlib.Path(__file__).resolve().parent / "_native" / library_file_name()
    return bundled


class GuiFormsError(Exception):
    """A refused call: its status and the calling thread's error detail."""

    def __init__(self, status: int, table_id: int, slot_index: int, message: str) -> None:
        super().__init__("GUI.Forms status " + str(status) + " (table " + str(table_id) + ", slot " +
                         str(slot_index) + "): " + message)
        self.status: int = status
        self.table_id: int = table_id
        self.slot_index: int = slot_index
        self.detail: str = message


class WrongThreadError(RuntimeError):
    """A UI call from a thread that is not the library's UI thread (the Python main thread)."""


class CallbackFailure(Exception):
    """A Python exception a callback raised, held until a Python caller gets control back."""

    def __init__(self, thrown: BaseException) -> None:
        super().__init__("a GUI.Forms callback raised " + type(thrown).__name__ + ": " + str(thrown))
        self.thrown: BaseException = thrown
        self.later_failures: list[CallbackFailure] = []


def field_type(record: type, name: str) -> type:
    """The ctypes type of record's field name, as the generated layer declared it."""
    for field_name, declared in record._fields_:
        if field_name == name:
            return declared
    raise KeyError(record.__name__ + " has no field " + name)


def unsupported_slot(*unused_arguments: object) -> int:
    return _abi.GF_STATUS_UNSUPPORTED_VERSION


class Table:
    """One negotiated function table: its record and its slots, each read once as an attribute."""

    def __init__(self, record: ctypes.Structure) -> None:
        self.record: ctypes.Structure = record
        served_size: int = record.struct_size
        for field_name, declared in type(record)._fields_:
            if not hasattr(declared, "argtypes"):
                continue
            offset: int = getattr(type(record), field_name).offset
            slot: object = getattr(record, field_name)
            if offset + ctypes.sizeof(declared) > served_size or not bool(slot):
                slot = unsupported_slot
            setattr(self, field_name, slot)


class Library:
    """The loaded library, its export and the tables negotiated so far."""

    def __init__(self, path: pathlib.Path) -> None:
        mismatches: list[str] = _abi.check_layout()
        if len(mismatches) > 0:
            raise RuntimeError("pyguiforms: ctypes lays out the ABI records differently: " + "; ".join(mismatches))
        if ctypes.sizeof(ctypes.c_void_p) != 8:
            raise RuntimeError("pyguiforms: the GUI.Forms C ABI supports 64-bit processes only")
        if not path.is_file():
            raise FileNotFoundError("pyguiforms: no GUI.Forms library at " + str(path) +
                                    " (set GUI_FORMS_ABI_LIBRARY, or install a platform wheel)")
        self.path: pathlib.Path = path
        self.handle: ctypes.CDLL = ctypes.CDLL(str(path))
        self.get_table = _abi.bind_gf_abi_get_table(self.handle)
        self.lock: threading.Lock = threading.Lock()
        self.tables: dict[str, Table] = {}
        self.runtime: Table = self.table("gf_runtime_table")

    def table(self, record_name: str) -> Table:
        """The table record_name, negotiated at the manifest's version on first use."""
        with self.lock:
            found: Table | None = self.tables.get(record_name)
            if found is not None:
                return found
            record_type: type = getattr(_abi, record_name)
            record: ctypes.Structure = record_type()
            table_id: int = _abi.TABLE_IDS[record_name]
            status: int = self.get_table(table_id, _abi.ABI_MAJOR, _abi.ABI_MINOR, ctypes.byref(record),
                                         ctypes.sizeof(record))
            if status != _abi.GF_STATUS_OK:
                raise GuiFormsError(status, table_id, _abi.GF_ABI_ENTRY_SLOT,
                                    record_name + " did not negotiate at ABI " + str(_abi.ABI_MAJOR) + "." +
                                    str(_abi.ABI_MINOR))
            negotiated: Table = Table(record)
            self.tables[record_name] = negotiated
        return negotiated

    def error_detail(self, status: int) -> GuiFormsError:
        """The calling thread's detail for status, which a refused call just answered."""
        capacity: int = 512
        for unused_attempt in range(2):
            detail: _abi.gf_error_detail = _abi.gf_error_detail()
            detail.struct_size = ctypes.sizeof(detail)
            message: ctypes.Array = ctypes.create_string_buffer(capacity)
            required: ctypes.c_uint64 = ctypes.c_uint64(0)
            read: int = self.runtime.error_detail(ctypes.byref(detail), message, capacity, ctypes.byref(required))
            if read == _abi.GF_STATUS_BUFFER_TOO_SMALL:
                capacity = required.value
                continue
            if read != _abi.GF_STATUS_OK or detail.status != status:
                break
            text: str = message.raw[:required.value].decode("utf-8", errors="replace")
            error: GuiFormsError = GuiFormsError(status, detail.table_id, detail.slot_index, text)
            return error
        return GuiFormsError(status, 0, 0, "(no error detail for this status)")

    def check(self, status: int) -> None:
        """Rethrows a callback failure kept for this thread, then raises for a status that is not OK."""
        registry.rethrow_pending()
        if status != _abi.GF_STATUS_OK:
            raise self.error_detail(status)


# ------------------------------------------------------------------- callbacks


class EventField:
    """One field of a lent event, copied out: its name, declared kind, flags and value."""

    def __init__(self, index: int, name: str, kind: int, flags: int, value: object) -> None:
        self.index: int = index
        self.name: str = name
        self.kind: int = kind
        self.flags: int = flags
        self.value: object = value

    def writable(self) -> bool:
        return (self.flags & _abi.GF_EVENT_FIELD_WRITABLE) != 0


class Event:
    """A gf_event lent for one invoke. Its fields are copied on first read; using it after the invoke raises."""

    def __init__(self, pointer: object) -> None:
        self.pointer: object | None = pointer
        self.copied_fields: list[EventField] | None = None

    def record(self) -> _abi.gf_event:
        if self.pointer is None:
            raise RuntimeError("a GUI.Forms event is lent only for its invoke")
        return self.pointer.contents

    @property
    def name(self) -> str:
        return values.read_view(self.record().name)

    @property
    def sender(self) -> int:
        return self.record().sender

    @property
    def payload(self) -> object:
        record: _abi.gf_event = self.record()
        if not bool(record.payload):
            return None
        return values.from_gf_value(record.payload.contents)

    @property
    def cancel(self) -> bool:
        return self.record().cancel != 0

    @cancel.setter
    def cancel(self, cancelled: bool) -> None:
        self.record().cancel = 1 if cancelled else 0

    def fields(self) -> list[EventField]:
        if self.copied_fields is not None:
            return self.copied_fields
        record: _abi.gf_event = self.record()
        copied: list[EventField] = []
        for index in range(record.field_count):
            field: _abi.gf_event_field = record.fields[index]
            value: object = None
            if bool(field.value):
                value = values.from_gf_value(field.value.contents)
            copied.append(EventField(index, values.read_view(field.name), field.kind, field.flags, value))
        self.copied_fields = copied
        return copied

    def field(self, name: str) -> object:
        """The value of the field name; KeyError when the event has none of that name."""
        for field in self.fields():
            if field.name == name:
                return field.value
        raise KeyError("the event " + self.name + " has no field " + name)

    def write(self, name: str, value: object) -> None:
        """Writes the writable field name (an enumeration by its value); the raiser reads it after the handlers."""
        for field in self.fields():
            if field.name != name:
                continue
            if not field.writable():
                raise AttributeError("the field " + name + " of " + self.name + " is read-only")
            holder: values.ValueHolder = values.to_gf_value(field.kind, value)
            session().write_field(self, field, holder)
            field.value = value
            return
        raise KeyError("the event " + self.name + " has no field " + name)

    def end(self) -> None:
        self.pointer = None


class CallbackRegistry:
    """The Python handlers lent to the library, by context key.

    A key is issued once and never reused; the library gives it back exactly
    once through release (gf_abi.h, Callbacks), which forgets the handler.
    The lock guards only the dictionary; no handler runs under it.
    Failures are kept per thread until a Python caller rethrows them.
    """

    MAXIMUM_KEY: int = (1 << 63) - 1

    def __init__(self) -> None:
        self.lock: threading.Lock = threading.Lock()
        self.next_key: int = 1
        self.handlers: dict[int, typing.Callable[[Event], None]] = {}
        self.failures: threading.local = threading.local()
        self.loop_failure: typing.Callable[[CallbackFailure], bool] | None = None

    def lend(self, handler: typing.Callable[[Event], None]) -> _abi.gf_callback:
        with self.lock:
            if self.next_key > CallbackRegistry.MAXIMUM_KEY:
                raise RuntimeError("pyguiforms: callback keys are exhausted")
            key: int = self.next_key
            self.next_key += 1
            self.handlers[key] = handler
        callback: _abi.gf_callback = _abi.gf_callback()
        callback.struct_size = ctypes.sizeof(callback)
        callback.reserved = 0
        callback.invoke = invoke_trampoline
        callback.release = release_trampoline
        callback.context = key
        return callback

    def forget(self, callback: _abi.gf_callback) -> None:
        """Forgets a callback the library refused (it never calls that one's release)."""
        with self.lock:
            self.handlers.pop(callback.context, None)

    def handler(self, key: int) -> typing.Callable[[Event], None]:
        with self.lock:
            found: typing.Callable[[Event], None] = self.handlers[key]
        return found

    def release(self, key: int) -> None:
        with self.lock:
            self.handlers.pop(key, None)

    def live_count(self) -> int:
        with self.lock:
            count: int = len(self.handlers)
        return count

    def pending(self) -> list[CallbackFailure]:
        found: list[CallbackFailure] | None = getattr(self.failures, "pending", None)
        if found is None:
            found = []
            self.failures.pending = found
        return found

    def record_failure(self, thrown: BaseException) -> None:
        # A failure a nested Python caller rethrew is already wrapped.
        failure: CallbackFailure = thrown if isinstance(thrown, CallbackFailure) else CallbackFailure(thrown)
        loop_failure: typing.Callable[[CallbackFailure], bool] | None = self.loop_failure
        if loop_failure is not None and loop_failure(failure):
            return
        self.pending().append(failure)

    def rethrow_pending(self) -> None:
        pending: list[CallbackFailure] = self.pending()
        if len(pending) == 0:
            return
        first: CallbackFailure = pending[0]
        first.later_failures = pending[1:]
        pending.clear()
        raise first from first.thrown


registry: CallbackRegistry = CallbackRegistry()


def invoke_callback(context: int | None, event_pointer: object) -> None:
    """The one invoke trampoline: runs the handler and lets no exception reach the library."""
    event: Event = Event(event_pointer)
    try:
        handler: typing.Callable[[Event], None] = registry.handler(context)
        handler(event)
    except BaseException as thrown:
        registry.record_failure(thrown)
    finally:
        event.end()


def release_callback(context: int | None) -> None:
    """The one release trampoline: forgets the handler."""
    try:
        registry.release(context)
    except BaseException as thrown:
        registry.record_failure(thrown)


# Made once for the process: the library may call them until it exits.
invoke_trampoline = field_type(_abi.gf_callback, "invoke")(invoke_callback)
release_trampoline = field_type(_abi.gf_callback, "release")(release_callback)


# ------------------------------------------------------------------- ownership

release_lock: threading.Lock = threading.Lock()


class ObjectReference:
    """One reference to a gf_object, given back exactly once."""

    def __init__(self, session: Session, identity: int) -> None:
        self.session: Session = session
        self.identity: int = identity

    def take(self) -> int:
        """Empties this reference and returns the identity it held (0 when already empty)."""
        with release_lock:
            identity: int = self.identity
            self.identity = 0
        return identity

    def release(self) -> None:
        identity: int = self.take()
        if identity != 0:
            self.session.objects.release(identity)

    def __enter__(self) -> ObjectReference:
        return self

    def __exit__(self, *unused_exception: object) -> None:
        self.release()

    def __del__(self) -> None:
        # A last resort: objects.release is callable from any thread, and the
        # library completes an ending on the UI thread (gf_abi.h, Threads).
        self.release()


class Subscription:
    """A subscription, ended once by disconnect, or by its source's disposal or destruction.

    It has no finalizer: a subscription lives until it is ended, not until
    its Python object goes, as a C# event handler stays connected.
    """

    def __init__(self, session: Session, identity: int) -> None:
        self.session: Session = session
        self.identity: int = identity

    def disconnect(self) -> None:
        with release_lock:
            identity: int = self.identity
            self.identity = 0
        if identity == 0:
            return
        status: int = self.session.events.disconnect(identity)
        if status != _abi.GF_STATUS_STALE_HANDLE:
            self.session.library.check(status)


# --------------------------------------------------------------------- session


def read_text_slot(library: Library, call: typing.Callable[[object, int, object], int]) -> str:
    """Runs a slot that copies text into a caller's buffer (buffer, capacity, required), growing it once."""
    capacity: int = 256
    for unused_attempt in range(2):
        buffer: ctypes.Array = ctypes.create_string_buffer(capacity)
        required: ctypes.c_uint64 = ctypes.c_uint64(0)
        status: int = call(buffer, capacity, ctypes.byref(required))
        if status == _abi.GF_STATUS_BUFFER_TOO_SMALL:
            capacity = required.value
            continue
        library.check(status)
        text: str = buffer.raw[:required.value].decode("utf-8")
        return text
    raise GuiFormsError(_abi.GF_STATUS_BUFFER_TOO_SMALL, 0, 0, "the text grew between two reads")


def read_value_slot(library: Library, call: typing.Callable[[object, object, int, object], int]) -> object:
    """Runs a slot that reads one gf_value (value, text buffer, capacity, required), growing the buffer once."""
    capacity: int = 256
    for unused_attempt in range(2):
        value: _abi.gf_value = _abi.gf_value()
        value.struct_size = ctypes.sizeof(value)
        buffer: ctypes.Array = ctypes.create_string_buffer(capacity)
        required: ctypes.c_uint64 = ctypes.c_uint64(0)
        status: int = call(ctypes.byref(value), buffer, capacity, ctypes.byref(required))
        if status == _abi.GF_STATUS_BUFFER_TOO_SMALL:
            capacity = required.value
            continue
        library.check(status)
        # The value's text points into buffer: copy it out while buffer lives.
        copied: object = values.from_gf_value(value)
        return copied
    raise GuiFormsError(_abi.GF_STATUS_BUFFER_TOO_SMALL, 0, 0, "the value's text grew between two reads")


class IndexedGetCall:
    """A named target for read_value_slot: properties.get_at for one object and index."""

    def __init__(self, slot: typing.Callable[..., int], identity: int, index: int) -> None:
        self.slot: typing.Callable[..., int] = slot
        self.identity: int = identity
        self.index: int = index

    def __call__(self, value: object, buffer: object, capacity: int, required: object) -> int:
        status: int = self.slot(self.identity, self.index, value, buffer, capacity, required)
        return status


class NamedGetCall:
    """A named target for read_value_slot: properties.get for one object and name."""

    def __init__(self, slot: typing.Callable[..., int], identity: int, name: str) -> None:
        self.slot: typing.Callable[..., int] = slot
        self.identity: int = identity
        self.name: bytes = name.encode("utf-8")

    def __call__(self, value: object, buffer: object, capacity: int, required: object) -> int:
        status: int = self.slot(self.identity, values.text_view(self.name), value, buffer, capacity, required)
        return status


class Session:
    """The process's one session: the tables, the UI thread, and one method per slot the Pythonic layer uses."""

    def __init__(self, library: Library) -> None:
        if threading.current_thread() is not threading.main_thread():
            raise WrongThreadError("pyguiforms: open the session on the main thread, which becomes the UI thread")
        self.library: Library = library
        self.ui_thread: threading.Thread = threading.current_thread()
        self.objects: Table = library.table("gf_objects_table")
        self.properties: Table = library.table("gf_properties_table")
        self.events: Table = library.table("gf_events_table")
        self.dispatch: Table = library.table("gf_dispatch_table")
        self.windows: Table = library.table("gf_windows_table")
        self.classes: Table = library.table("gf_classes_table")
        self.controls: Table = library.table("gf_controls_table")
        self.schema: Table = library.table("gf_schema_table")
        self.schema_cache: schema.SchemaCache = schema.SchemaCache(self.schema, self.check)
        self.running_root: int = 0
        self.failure_hook: typing.Callable[[CallbackFailure], bool] | None = None
        self.class_tables: dict[str, ctypes.Structure] = {}
        self.class_tables_lock: threading.Lock = threading.Lock()

    def require_ui_thread(self) -> None:
        if threading.current_thread() is not self.ui_thread:
            raise WrongThreadError("pyguiforms: this call runs on the UI thread (the main thread) only; "
                                   "post work there with Session.begin_invoke")

    def check(self, status: int) -> None:
        self.library.check(status)

    def version(self) -> tuple[int, int, int, int, int]:
        """(library major, minor, patch, ABI major, ABI minor)."""
        info: _abi.gf_abi_version_info = _abi.gf_abi_version_info()
        info.struct_size = ctypes.sizeof(info)
        self.check(self.library.runtime.version(ctypes.byref(info)))
        version: tuple[int, int, int, int, int] = (info.library_major, info.library_minor, info.library_patch,
                                                   info.abi_major, info.abi_minor)
        return version

    # Objects.

    def create(self, type_name: str, stable_id: str) -> ObjectReference:
        self.require_ui_thread()
        type_bytes: bytes = type_name.encode("utf-8")
        id_bytes: bytes = stable_id.encode("utf-8")
        identity: ctypes.c_uint64 = ctypes.c_uint64(0)
        self.check(self.objects.create(values.text_view(type_bytes), values.text_view(id_bytes),
                                       ctypes.byref(identity)))
        reference: ObjectReference = ObjectReference(self, identity.value)
        return reference

    def create_with_owner(self, type_name: str, stable_id: str, owner: int) -> ObjectReference:
        self.require_ui_thread()
        type_bytes: bytes = type_name.encode("utf-8")
        id_bytes: bytes = stable_id.encode("utf-8")
        arguments: _abi.gf_create_arguments = _abi.gf_create_arguments()
        arguments.struct_size = ctypes.sizeof(arguments)
        arguments.owner = owner
        identity: ctypes.c_uint64 = ctypes.c_uint64(0)
        self.check(self.objects.create_with(values.text_view(type_bytes), values.text_view(id_bytes),
                                            ctypes.byref(arguments), ctypes.byref(identity)))
        reference: ObjectReference = ObjectReference(self, identity.value)
        return reference

    def create_from_class(self, class_record_name: str, class_id: int, stable_id: str) -> ObjectReference:
        """Creates class_id's stock type through an override-free class table, so its raisers have bases.

        The table is borrowed by every object made from it (gf_abi_classes.h,
        classes.create), so the session keeps one per class for its life.
        """
        self.require_ui_thread()
        with self.class_tables_lock:
            table: ctypes.Structure | None = self.class_tables.get(class_record_name)
            if table is None:
                table = getattr(_abi, class_record_name)()
                table.header.struct_size = ctypes.sizeof(_abi.gf_class_header)
                table.header.abi_minor = _abi.ABI_MINOR
                table.header.class_id = class_id
                table.header.segment_count = 0
                self.class_tables[class_record_name] = table
        id_bytes: bytes = stable_id.encode("utf-8")
        identity: ctypes.c_uint64 = ctypes.c_uint64(0)
        self.check(self.classes.create(ctypes.byref(table.header), values.text_view(id_bytes), None,
                                       ctypes.byref(identity)))
        reference: ObjectReference = ObjectReference(self, identity.value)
        return reference

    def type_id(self, identity: int) -> str:
        self.require_ui_thread()
        text: str = read_text_slot(self.library, ObjectTextCall(self.objects.type_id, identity))
        return text

    def stable_id(self, identity: int) -> str:
        self.require_ui_thread()
        text: str = read_text_slot(self.library, ObjectTextCall(self.objects.stable_id, identity))
        return text

    def dispose(self, identity: int) -> None:
        self.require_ui_thread()
        self.check(self.objects.dispose(identity))

    def insert_child(self, parent: int, child: int, index: int) -> None:
        self.require_ui_thread()
        self.check(self.objects.insert_child(parent, child, index))

    def remove_child(self, parent: int, child: int) -> None:
        self.require_ui_thread()
        self.check(self.objects.remove_child(parent, child))

    def child_count(self, parent: int) -> int:
        self.require_ui_thread()
        count: ctypes.c_uint64 = ctypes.c_uint64(0)
        self.check(self.objects.child_count(parent, ctypes.byref(count)))
        return count.value

    def child_at(self, parent: int, index: int) -> ObjectReference:
        self.require_ui_thread()
        child: ctypes.c_uint64 = ctypes.c_uint64(0)
        self.check(self.objects.child_at(parent, index, ctypes.byref(child)))
        reference: ObjectReference = ObjectReference(self, child.value)
        return reference

    def parent(self, identity: int) -> ObjectReference | None:
        self.require_ui_thread()
        found: ctypes.c_uint64 = ctypes.c_uint64(0)
        self.check(self.objects.parent(identity, ctypes.byref(found)))
        if found.value == 0:
            return None
        reference: ObjectReference = ObjectReference(self, found.value)
        return reference

    # Properties.

    def get_property(self, identity: int, index: int) -> object:
        """The value of property index (its position in the object's schema type), copied out."""
        self.require_ui_thread()
        value: object = read_value_slot(self.library, IndexedGetCall(self.properties.get_at, identity, index))
        return value

    def get_property_by_name(self, identity: int, name: str) -> object:
        """The value of the property name, for one the schema type does not list; copied out."""
        self.require_ui_thread()
        value: object = read_value_slot(self.library, NamedGetCall(self.properties.get, identity, name))
        return value

    def read_elements(self, identity: int, name: str, count: int) -> list[object]:
        """The count elements of the COLLECTION property name, copied out."""
        self.require_ui_thread()
        name_bytes: bytes = name.encode("utf-8")
        elements: list[object] = []
        if count == 0:
            return elements
        capacity: int = 1024
        for unused_attempt in range(2):
            records: ctypes.Array = (_abi.gf_value * count)()
            for index in range(count):
                records[index].struct_size = ctypes.sizeof(_abi.gf_value)
            buffer: ctypes.Array = ctypes.create_string_buffer(capacity)
            required: ctypes.c_uint64 = ctypes.c_uint64(0)
            status: int = self.properties.read_elements(identity, values.text_view(name_bytes), 0, count, records,
                                                        buffer, capacity, ctypes.byref(required))
            if status == _abi.GF_STATUS_BUFFER_TOO_SMALL:
                capacity = required.value
                continue
            self.check(status)
            for index in range(count):
                elements.append(values.from_gf_value(records[index]))
            return elements
        raise GuiFormsError(_abi.GF_STATUS_BUFFER_TOO_SMALL, 0, 0, "the collection's text grew between two reads")

    def set_property(self, identity: int, index: int, holder: values.ValueHolder) -> None:
        self.require_ui_thread()
        self.check(self.properties.set_at(identity, index, holder.reference()))

    def set_property_by_name(self, identity: int, name: str, holder: values.ValueHolder) -> None:
        self.require_ui_thread()
        name_bytes: bytes = name.encode("utf-8")
        self.check(self.properties.set(identity, values.text_view(name_bytes), holder.reference()))

    def reset_property(self, identity: int, name: str) -> None:
        self.require_ui_thread()
        name_bytes: bytes = name.encode("utf-8")
        self.check(self.properties.reset(identity, values.text_view(name_bytes)))

    # Events and dispatch.

    def subscribe(self, source: int, interaction: str, handler: typing.Callable[[Event], None],
                  property_change: bool) -> Subscription:
        self.require_ui_thread()
        name_bytes: bytes = interaction.encode("utf-8")
        callback: _abi.gf_callback = registry.lend(handler)
        identity: ctypes.c_uint64 = ctypes.c_uint64(0)
        slot = self.events.subscribe_property if property_change else self.events.subscribe
        status: int = slot(source, values.text_view(name_bytes), ctypes.byref(callback), ctypes.byref(identity))
        if status != _abi.GF_STATUS_OK:
            registry.forget(callback)
        self.check(status)
        subscription: Subscription = Subscription(self, identity.value)
        return subscription

    def write_field(self, event: Event, field: EventField, holder: values.ValueHolder) -> None:
        self.require_ui_thread()
        if event.pointer is None:
            raise RuntimeError("a GUI.Forms event is lent only for its invoke")
        self.check(self.events.write_field(event.pointer, field.index, holder.reference()))

    def begin_invoke(self, target: int, handler: typing.Callable[[Event], None]) -> None:
        """Posts handler to the UI thread with sender target; any thread may call it."""
        callback: _abi.gf_callback = registry.lend(handler)
        status: int = self.dispatch.begin_invoke(target, ctypes.byref(callback))
        if status != _abi.GF_STATUS_OK:
            registry.forget(callback)
            raise self.library.error_detail(status)

    def run_pending(self) -> int:
        self.require_ui_thread()
        invoked: ctypes.c_uint64 = ctypes.c_uint64(0)
        self.check(self.dispatch.run_pending(ctypes.byref(invoked)))
        return invoked.value

    def raise_hook(self, identity: int, class_id: int, entry: int, event_name: str) -> int:
        """Runs a raiser's base for identity outside an entry (C#'s OnX called directly); returns the status."""
        self.require_ui_thread()
        raiser: _abi.gf_base_raiser = _abi.gf_base_raiser()
        status: int = self.classes.base_raiser(class_id, entry, ctypes.byref(raiser))
        if status != _abi.GF_STATUS_OK:
            return status
        event: _abi.gf_event = _abi.gf_event()
        event.struct_size = ctypes.sizeof(event)
        name_bytes: bytes = event_name.encode("utf-8")
        event.name = values.text_view(name_bytes)
        called: int = raiser(identity, ctypes.byref(event))
        return called

    # Layout.

    def suspend_layout(self, identity: int) -> None:
        self.require_ui_thread()
        self.check(self.controls.suspend_layout(identity))

    def resume_layout(self, identity: int, perform_layout: bool) -> None:
        self.require_ui_thread()
        self.check(self.controls.resume_layout(identity, 1 if perform_layout else 0))

    def focus(self, identity: int) -> bool:
        self.require_ui_thread()
        focused: ctypes.c_uint32 = ctypes.c_uint32(0)
        self.check(self.controls.focus(identity, ctypes.byref(focused)))
        return focused.value != 0

    # The window's run.

    def loop_failure(self, failure: CallbackFailure) -> bool:
        """The event loop's failure rule; True when the program's hook handled it and the loop carries on."""
        hook: typing.Callable[[CallbackFailure], bool] | None = self.failure_hook
        if hook is not None:
            try:
                if hook(failure):
                    return True
            except BaseException as thrown:
                failure = CallbackFailure(thrown)
                registry.pending().append(failure)
        if self.running_root != 0:
            self.windows.request_close(self.running_root)
        return False

    def request_close(self, root: int) -> None:
        self.require_ui_thread()
        self.check(self.windows.request_close(root))

    def run(self, root: int, title: str, width: float, height: float, minimum_width: float, minimum_height: float,
            ready: typing.Callable[[Event], None] | None, closing: typing.Callable[[Event], None] | None,
            closed: typing.Callable[[Event], None] | None) -> None:
        """Runs root's window until it closes; a callback's failure closes it and is raised here."""
        self.require_ui_thread()
        title_bytes: bytes = title.encode("utf-8")
        options: _abi.gf_run_options = _abi.gf_run_options()
        options.struct_size = ctypes.sizeof(options)
        options.flags = _abi.GF_RUN_FLAGS_NONE
        options.title = values.text_view(title_bytes)
        options.width = width
        options.height = height
        options.minimum_width = minimum_width
        options.minimum_height = minimum_height
        lent: list[_abi.gf_callback] = []
        handlers: tuple = ((ready, "ready"), (closing, "closing"), (closed, "closed"))
        for handler, slot_name in handlers:
            if handler is None:
                continue
            callback: _abi.gf_callback = registry.lend(handler)
            lent.append(callback)
            setattr(options, slot_name, ctypes.pointer(callback))
        self.running_root = root
        registry.loop_failure = self.loop_failure
        try:
            status: int = self.windows.run(root, ctypes.byref(options))
        finally:
            registry.loop_failure = None
            self.running_root = 0
        if status != _abi.GF_STATUS_OK:
            for callback in lent:
                registry.forget(callback)
        self.check(status)


class ObjectTextCall:
    """A named target for read_text_slot: one object's type_id or stable_id slot."""

    def __init__(self, slot: typing.Callable[..., int], identity: int) -> None:
        self.slot: typing.Callable[..., int] = slot
        self.identity: int = identity

    def __call__(self, buffer: object, capacity: int, required: object) -> int:
        status: int = self.slot(self.identity, buffer, capacity, required)
        return status


# The process's session: one per process, as the library has one registry per process (gf_abi.h, H3).
session_lock: threading.Lock = threading.Lock()
opened_session: Session | None = None


def session() -> Session:
    """The process's session, opened on first use (on the main thread)."""
    global opened_session
    with session_lock:
        if opened_session is None:
            opened_session = Session(Library(find_library()))
        found: Session = opened_session
    return found


def set_failure_hook(hook: typing.Callable[[CallbackFailure], bool] | None) -> None:
    """Sets what a callback's failure under the event loop does first.

    The hook receives the failure; returning True handles it, and the loop
    carries on. Returning False (or raising) keeps the default rule: the
    running window is asked to close and run raises the failure.
    """
    session().failure_hook = hook
