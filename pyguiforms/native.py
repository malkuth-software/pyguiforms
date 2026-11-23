"""pyguiforms' hand-written layer over the generated 1:1 layer (``_abi``).

It adds the invariants the C ABI leaves to its caller, and nothing else:

- Loading: the one library, ``gui_forms_abi1`` (``libgui_forms_abi.1.dylib``,
  ``libgui_forms_abi.so.1``, ``gui_forms_abi1.dll``), found by
  ``GUI_FORMS_ABI_LIBRARY`` or beside the package, and kept loaded for the
  process (the tables it lends point into it).
- Negotiation: each table is negotiated once at the manifest's version. A slot
  the library did not serve (past the negotiated struct_size, or null)
  answers GF_STATUS_UNSUPPORTED_VERSION instead of calling through null, as
  gui_forms ``gf_abi.hpp`` does.
- Failures: a refused call becomes ``GuiFormsError`` with the calling
  thread's error detail; only the caller knows which statuses it expects, so
  ``check`` is called where a failure is exceptional.
- Callbacks: one module-level trampoline per callback slot type, made once
  for the process, so lending a callback allocates no executable closure. A
  callback's context is a key into ``CallbackRegistry``, issued once and never
  reused; the library's release forgets it. No Python exception crosses into
  the library: the trampoline catches it, records it as a ``CallbackFailure``
  for the thread, and the Python caller that gets control back next rethrows
  it (``check``, or ``run`` after the loop ends; see ``Session.run``).
- Ownership: ``ObjectReference`` holds one reference to a ``gf_object`` and
  gives it back exactly once (``release``, the context manager, or the
  finalizer as a last resort; objects.release is callable from any thread).

Threads: the thread that creates the first object is the library's UI thread
(gf_abi.h, Threads). ctypes releases the GIL around every library call and
takes it again in every trampoline, so other Python threads run while the
event loop waits, and a callback holds the GIL while it runs.
"""

from __future__ import annotations

import ctypes
import os
import pathlib
import sys
import threading

from pyguiforms import _abi

# ---------------------------------------------------------------- the library


def library_file_name() -> str:
    """The file cmake/CAbi.cmake builds for this platform and ABI major."""
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


class CallbackFailure(Exception):
    """A Python exception a callback raised, held until a Python caller gets control back."""

    def __init__(self, thrown: BaseException) -> None:
        super().__init__("a GUI.Forms callback raised " + type(thrown).__name__ + ": " + str(thrown))
        self.thrown: BaseException = thrown


def field_type(record: type, name: str) -> type:
    """The ctypes type of record's field name, as the generated layer declared it."""
    for field_name, declared in record._fields_:
        if field_name == name:
            return declared
    raise KeyError(record.__name__ + " has no field " + name)


def unsupported_slot(*unused_arguments: object) -> int:
    return _abi.GF_STATUS_UNSUPPORTED_VERSION


class Table:
    """One negotiated function table: its record and its slots, each bound once.

    Reading a CFUNCTYPE field from a ctypes.Structure builds a new function
    object on every access (ctypes has no original-object return), so the
    slots are read once here and kept as attributes of this object.
    """

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
        self.path: pathlib.Path = path
        self.handle: ctypes.CDLL = ctypes.CDLL(str(path))
        self.get_table = _abi.bind_gf_abi_get_table(self.handle)
        self.tables: dict[str, Table] = {}
        self.runtime: Table = self.table("gf_runtime_table")

    def table(self, record_name: str) -> Table:
        """The table record_name, negotiated at the manifest's version on first use."""
        if record_name in self.tables:
            return self.tables[record_name]
        record_type: type = getattr(_abi, record_name)
        record: ctypes.Structure = record_type()
        status: int = self.get_table(_abi.TABLE_IDS[record_name], _abi.ABI_MAJOR, _abi.ABI_MINOR,
                                     ctypes.byref(record), ctypes.sizeof(record))
        if status != _abi.GF_STATUS_OK:
            raise GuiFormsError(status, _abi.TABLE_IDS[record_name], _abi.GF_ABI_ENTRY_SLOT,
                                record_name + " did not negotiate at ABI " + str(_abi.ABI_MAJOR) + "." +
                                str(_abi.ABI_MINOR))
        negotiated: Table = Table(record)
        self.tables[record_name] = negotiated
        return negotiated

    def error_detail(self, status: int) -> GuiFormsError:
        detail: _abi.gf_error_detail = _abi.gf_error_detail()
        detail.struct_size = ctypes.sizeof(detail)
        message: ctypes.Array = ctypes.create_string_buffer(512)
        required: ctypes.c_uint64 = ctypes.c_uint64(0)
        read: int = self.runtime.error_detail(ctypes.byref(detail), message, len(message), ctypes.byref(required))
        if read != _abi.GF_STATUS_OK:
            return GuiFormsError(status, 0, 0, "(no error detail)")
        text: str = message.raw[:required.value].decode("utf-8", errors="replace")
        error: GuiFormsError = GuiFormsError(status, detail.table_id, detail.slot_index, text)
        return error

    def check(self, status: int) -> None:
        """Rethrows a callback failure kept for this thread, then raises for a status that is not OK."""
        registry.rethrow_pending()
        if status != _abi.GF_STATUS_OK:
            raise self.error_detail(status)


# ------------------------------------------------------------------------ text


class Utf8Text:
    """UTF-8 bytes and a gf_utf8_view of them; the view is valid while this object lives."""

    def __init__(self, text: str) -> None:
        self.encoded: bytes = text.encode("utf-8")
        self.view: _abi.gf_utf8_view = _abi.gf_utf8_view()
        self.view.data = ctypes.cast(ctypes.c_char_p(self.encoded), ctypes.POINTER(ctypes.c_char))
        self.view.size = len(self.encoded)


def read_view(view: _abi.gf_utf8_view) -> str:
    """Copies a lent view's text out (an empty view may have a null data pointer)."""
    if view.size == 0:
        return ""
    copied: bytes = ctypes.string_at(view.data, view.size)
    return copied.decode("utf-8")


# ------------------------------------------------------------------- callbacks


class Event:
    """A gf_event lent for one invoke. Reading it after the invoke has returned raises."""

    def __init__(self, pointer: ctypes._Pointer) -> None:
        self.pointer: ctypes._Pointer | None = pointer

    def record(self) -> _abi.gf_event:
        if self.pointer is None:
            raise RuntimeError("a GUI.Forms event is lent only for its invoke")
        return self.pointer.contents

    def name(self) -> str:
        return read_view(self.record().name)

    def sender(self) -> int:
        return self.record().sender

    def field_text(self, wanted: str) -> str | None:
        """The text of field wanted (an ENUMERATION's choice name, or TEXT), or None when absent."""
        event: _abi.gf_event = self.record()
        for index in range(event.field_count):
            field: _abi.gf_event_field = event.fields[index]
            if read_view(field.name) != wanted or not bool(field.value):
                continue
            return read_view(field.value.contents.text)
        return None

    def end(self) -> None:
        self.pointer = None


class CallbackRegistry:
    """The Python handlers lent to the library, by context key.

    A key is issued once and never reused; the library gives it back exactly
    once through release (gf_abi.h, Callbacks), which forgets the handler.
    Failures are kept per thread until a Python caller rethrows them.
    """

    MAXIMUM_KEY: int = (1 << 63) - 1

    def __init__(self) -> None:
        self.lock: threading.Lock = threading.Lock()
        self.next_key: int = 1
        self.handlers: dict[int, object] = {}
        self.failures: threading.local = threading.local()
        self.on_failure_in_loop: object | None = None

    def lend(self, handler: object) -> _abi.gf_callback:
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

    def handler(self, key: int) -> object:
        with self.lock:
            found: object = self.handlers[key]
        return found

    def release(self, key: int) -> None:
        with self.lock:
            self.handlers.pop(key, None)

    def live_count(self) -> int:
        with self.lock:
            count: int = len(self.handlers)
        return count

    def record_failure(self, thrown: BaseException) -> None:
        pending: list[CallbackFailure] = getattr(self.failures, "pending", [])
        # A failure a nested Python caller rethrew is already wrapped.
        if isinstance(thrown, CallbackFailure):
            pending.append(thrown)
        else:
            pending.append(CallbackFailure(thrown))
        self.failures.pending = pending
        if self.on_failure_in_loop is not None:
            self.on_failure_in_loop()

    def rethrow_pending(self) -> None:
        pending: list[CallbackFailure] = getattr(self.failures, "pending", [])
        if len(pending) == 0:
            return
        self.failures.pending = []
        first: CallbackFailure = pending[0]
        first.later_failures = pending[1:]
        raise first from first.thrown


registry: CallbackRegistry = CallbackRegistry()


def invoke_callback(context: int | None, event_pointer: ctypes._Pointer) -> None:
    """The one invoke trampoline: runs the handler and lets no exception reach the library."""
    event: Event = Event(event_pointer)
    try:
        handler: object = registry.handler(context)
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


class ObjectReference:
    """One reference to a gf_object, given back exactly once."""

    def __init__(self, session: Session, identity: int) -> None:
        self.session: Session = session
        self.identity: int = identity

    def release(self) -> None:
        if self.identity == 0:
            return
        identity: int = self.identity
        self.identity = 0
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
    """A subscription, ended exactly once by disconnect (or by its source's end)."""

    def __init__(self, session: Session, identity: int) -> None:
        self.session: Session = session
        self.identity: int = identity

    def disconnect(self) -> None:
        if self.identity == 0:
            return
        identity: int = self.identity
        self.identity = 0
        status: int = self.session.events.disconnect(identity)
        if status != _abi.GF_STATUS_STALE_HANDLE:
            self.session.library.check(status)


# --------------------------------------------------------------------- session


class Session:
    """The tables a program uses and the operations the prototype needs, each one slot call."""

    def __init__(self, library: Library) -> None:
        self.library: Library = library
        self.objects: Table = library.table("gf_objects_table")
        self.properties: Table = library.table("gf_properties_table")
        self.events: Table = library.table("gf_events_table")
        self.dispatch: Table = library.table("gf_dispatch_table")
        self.windows: Table = library.table("gf_windows_table")
        self.classes: Table = library.table("gf_classes_table")
        self.running_root: int = 0
        self.class_tables: dict[str, ctypes.Structure] = {}

    def version(self) -> str:
        info: _abi.gf_abi_version_info = _abi.gf_abi_version_info()
        info.struct_size = ctypes.sizeof(info)
        self.library.check(self.library.runtime.version(ctypes.byref(info)))
        text: str = ("GUI.Forms " + str(info.library_major) + "." + str(info.library_minor) + "." +
                     str(info.library_patch) + ", C ABI " + str(info.abi_major) + "." + str(info.abi_minor))
        return text

    def create(self, type_name: str, stable_id: str) -> ObjectReference:
        type_text: Utf8Text = Utf8Text(type_name)
        id_text: Utf8Text = Utf8Text(stable_id)
        identity: _abi.gf_object = _abi.gf_object(0)
        self.library.check(self.objects.create(type_text.view, id_text.view, ctypes.byref(identity)))
        reference: ObjectReference = ObjectReference(self, identity.value)
        return reference

    def create_from_class(self, class_record_name: str, class_id: int, stable_id: str) -> ObjectReference:
        """Creates class_id's stock type through an override-free class table, so its raisers have bases.

        The table is borrowed by every object made from it (gf_abi_classes.h,
        classes.create), so the session keeps one per class for its life.
        """
        table: ctypes.Structure | None = self.class_tables.get(class_record_name)
        if table is None:
            table = getattr(_abi, class_record_name)()
            table.header.struct_size = ctypes.sizeof(_abi.gf_class_header)
            table.header.abi_minor = _abi.ABI_MINOR
            table.header.class_id = class_id
            table.header.segment_count = 0
            self.class_tables[class_record_name] = table
        id_text: Utf8Text = Utf8Text(stable_id)
        identity: _abi.gf_object = _abi.gf_object(0)
        self.library.check(self.classes.create(ctypes.byref(table.header), id_text.view, None,
                                               ctypes.byref(identity)))
        reference: ObjectReference = ObjectReference(self, identity.value)
        return reference

    def insert_child(self, parent: ObjectReference, child: ObjectReference, index: int) -> None:
        self.library.check(self.objects.insert_child(parent.identity, child.identity, index))

    def set_text(self, target: ObjectReference, name: str, text: str) -> None:
        name_text: Utf8Text = Utf8Text(name)
        value_text: Utf8Text = Utf8Text(text)
        value: _abi.gf_value = _abi.gf_value()
        value.struct_size = ctypes.sizeof(value)
        value.kind = _abi.GF_VALUE_KIND_TEXT
        value.text = value_text.view
        self.library.check(self.properties.set(target.identity, name_text.view, ctypes.byref(value)))

    def set_rectangle(self, target: ObjectReference, name: str, x: float, y: float, width: float,
                      height: float) -> None:
        name_text: Utf8Text = Utf8Text(name)
        value: _abi.gf_value = _abi.gf_value()
        value.struct_size = ctypes.sizeof(value)
        value.kind = _abi.GF_VALUE_KIND_RECTANGLE
        value.rectangle.x = x
        value.rectangle.y = y
        value.rectangle.width = width
        value.rectangle.height = height
        self.library.check(self.properties.set(target.identity, name_text.view, ctypes.byref(value)))

    def subscribe(self, source: ObjectReference, interaction: str, handler: object) -> Subscription:
        name_text: Utf8Text = Utf8Text(interaction)
        callback: _abi.gf_callback = registry.lend(handler)
        identity: _abi.gf_subscription = _abi.gf_subscription(0)
        status: int = self.events.subscribe(source.identity, name_text.view, ctypes.byref(callback),
                                            ctypes.byref(identity))
        if status != _abi.GF_STATUS_OK:
            registry.forget(callback)
        self.library.check(status)
        subscription: Subscription = Subscription(self, identity.value)
        return subscription

    def begin_invoke(self, target: ObjectReference, handler: object) -> None:
        """Posts handler to the UI thread; any thread may call it."""
        callback: _abi.gf_callback = registry.lend(handler)
        status: int = self.dispatch.begin_invoke(target.identity, ctypes.byref(callback))
        if status != _abi.GF_STATUS_OK:
            registry.forget(callback)
            raise self.library.error_detail(status)

    def raise_click(self, target: ObjectReference) -> None:
        """Runs Control::on_click's base for target, as C#'s OnClick called directly does."""
        entry: int = control_hook_entry("on_click")
        raiser: _abi.gf_base_raiser = _abi.gf_base_raiser()
        self.library.check(self.classes.base_raiser(_abi.GF_CLASS_CONTROL, entry, ctypes.byref(raiser)))
        event: _abi.gf_event = _abi.gf_event()
        event.struct_size = ctypes.sizeof(event)
        click_text: Utf8Text = Utf8Text("click")
        event.name = click_text.view
        self.library.check(raiser(target.identity, ctypes.byref(event)))

    def request_close(self) -> None:
        self.library.check(self.windows.request_close(self.running_root))

    def close_after_failure(self) -> None:
        """The loop's failure policy: ask the running window to close, so run returns and rethrows."""
        if self.running_root != 0:
            self.windows.request_close(self.running_root)

    def run(self, root: ObjectReference, title: str, width: float, height: float, ready: object | None,
            closing: object | None, closed: object | None) -> None:
        """Runs root's window until it closes; a callback's failure closes it and is raised here."""
        title_text: Utf8Text = Utf8Text(title)
        options: _abi.gf_run_options = _abi.gf_run_options()
        options.struct_size = ctypes.sizeof(options)
        options.flags = _abi.GF_RUN_FLAGS_NONE
        options.title = title_text.view
        options.width = width
        options.height = height
        lent: list[_abi.gf_callback] = []
        for handler, slot_name in ((ready, "ready"), (closing, "closing"), (closed, "closed")):
            if handler is None:
                continue
            callback: _abi.gf_callback = registry.lend(handler)
            lent.append(callback)
            setattr(options, slot_name, ctypes.pointer(callback))
        self.running_root = root.identity
        registry.on_failure_in_loop = self.close_after_failure
        try:
            status: int = self.windows.run(root.identity, ctypes.byref(options))
        finally:
            registry.on_failure_in_loop = None
            self.running_root = 0
        if status != _abi.GF_STATUS_OK:
            for callback in lent:
                registry.forget(callback)
        self.library.check(status)

    def run_pending(self) -> int:
        invoked: ctypes.c_uint64 = ctypes.c_uint64(0)
        self.library.check(self.dispatch.run_pending(ctypes.byref(invoked)))
        return invoked.value


def control_hook_entry(name: str) -> int:
    """name's entry index in Control's segment: its slot after the 8-byte segment header."""
    size, offsets = _abi.LAYOUT["gf_control_hooks"]
    for field_name, offset in offsets:
        if field_name == name:
            return (offset - 8) // 8
    raise KeyError("gf_control_hooks has no entry " + name)


def open_session() -> Session:
    library: Library = Library(find_library())
    session: Session = Session(library)
    return session
