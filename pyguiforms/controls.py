"""The Pythonic layer's base classes: a component, a control and a schema property.

Every class in ``_controls`` derives from ``Component`` (components and
services) or ``Control`` (controls), and declares the schema's properties
as ``Property`` descriptors under the schema's names, so ``button.text``
reads the ``text`` property and ``button.text = "OK"`` writes it.

Ownership: a component holds one reference to its object and gives it back
once, by ``release`` (or the context manager, which disposes first). A
control's children are kept by their parent's Python object, as the
library's tree keeps them, so a window's controls live while it does.

Events: ``on(name)`` is a decorator that subscribes a function to one of
the type's interactions (``INTERACTIONS``, the schema's names);
``on_change(name)`` subscribes to a property's change. A handler receives
the ``native.Event``, lent for the call. Subscriptions end when the object
is disposed or destroyed, or by ``Subscription.disconnect``.
"""

from __future__ import annotations

import contextlib
import ctypes
import threading
import typing

from pyguiforms import _abi
from pyguiforms import native
from pyguiforms import schema
from pyguiforms import values

Handler = typing.Callable[[native.Event], None]


class Property:
    """One schema property as a descriptor.

    It carries what the pinned schema says of it: the name, the kind word,
    whether it is writable and bindable, an enumeration's choice names, and
    whether it is a content value (a font or colour that is the control's
    content, not its look). The form-document loader checks documents
    against these; the library's own schema decides at run time.
    """

    def __init__(self, name: str, kind: str, writable: bool, doc: str, choices: tuple[str, ...] = (),
                 bindable: bool = False, content: bool = False) -> None:
        self.name: str = name
        self.kind: str = kind
        self.writable: bool = writable
        self.choices: tuple[str, ...] = choices
        self.bindable: bool = bindable
        self.content: bool = content
        self.__doc__ = doc

    def __get__(self, component: Component | None, owner: type) -> object:
        if component is None:
            return self
        value: object = component.get(self.name)
        return value

    def __set__(self, component: Component, value: object) -> None:
        if not self.writable:
            raise AttributeError(self.name + " is read-only")
        component.set(self.name, value)


class StableIds:
    """Issues the stable IDs of components created without one, each once.

    A stable ID is lowercase letters and digits joined by single '-' (gf_abi.h,
    objects.create), so the type ID's '_' becomes '-': "text-box12".
    """

    MAXIMUM: int = (1 << 63) - 1

    def __init__(self) -> None:
        self.lock: threading.Lock = threading.Lock()
        self.next_number: int = 1

    def issue(self, type_id: str) -> str:
        with self.lock:
            if self.next_number > StableIds.MAXIMUM:
                raise RuntimeError("pyguiforms: automatic stable IDs are exhausted")
            number: int = self.next_number
            self.next_number += 1
        return type_id.replace("_", "-") + str(number)


stable_ids: StableIds = StableIds()


class Raiser:
    """Where an interaction's raiser lives: the class whose hooks segment has its on_<name> entry, and the entry."""

    def __init__(self, class_id: int, entry: int) -> None:
        self.class_id: int = class_id
        self.entry: int = entry


def hook_raisers() -> dict[str, Raiser]:
    """Every on_<name> entry of the generated hooks segments (gf_<class>_hooks), by interaction name.

    An entry's index is its position after the segment's struct_size and
    class_id (gf_abi_classes.h, Hooks), which is how classes.base_raiser
    numbers it. A name two segments declare keeps the more basic class's
    entry: Control's on_click, not a subclass's.
    """
    found: dict[str, Raiser] = {}
    for record_name in sorted(dir(_abi)):
        if not record_name.startswith("gf_") or not record_name.endswith("_hooks"):
            continue
        class_name: str = "GF_CLASS_" + record_name[len("gf_"):-len("_hooks")].upper()
        class_id: int | None = getattr(_abi, class_name, None)
        if class_id is None:
            continue
        record: type = getattr(_abi, record_name)
        first_entry: int = getattr(record, "class_id").offset + ctypes.sizeof(ctypes.c_uint32)
        for field_name, unused_type in record._fields_:
            if not field_name.startswith("on_"):
                continue
            entry: int = (getattr(record, field_name).offset - first_entry) // ctypes.sizeof(ctypes.c_void_p)
            name: str = field_name[len("on_"):]
            known: Raiser | None = found.get(name)
            if known is None or class_id < known.class_id:
                found[name] = Raiser(class_id, entry)
    return found


RAISERS: dict[str, Raiser] = hook_raisers()


class Component:
    """An object of one schema type, made through its class table when it has one, so its raisers have bases."""

    __slots__ = ("session", "reference", "type_info", "subscriptions", "stable_id", "__weakref__")

    TYPE_ID: str = ""
    INTERACTIONS: tuple[str, ...] = ()

    def __init__(self, stable_id: str | None = None, **properties: object) -> None:
        if self.TYPE_ID == "":
            raise TypeError("pyguiforms: create a schema type's class, not " + type(self).__name__)
        self.session: native.Session = native.session()
        self.stable_id: str = stable_id if stable_id is not None else stable_ids.issue(self.TYPE_ID)
        self.reference: native.ObjectReference = self.create()
        self.type_info: schema.TypeInfo = self.session.schema_cache.type_info(self.TYPE_ID)
        self.subscriptions: list[native.Subscription] = []
        for name, value in properties.items():
            self.set(name, value)

    def create(self) -> native.ObjectReference:
        class_record: str = "gf_" + self.TYPE_ID + "_class"
        class_id: int | None = getattr(_abi, "GF_CLASS_" + self.TYPE_ID.upper(), None)
        if hasattr(_abi, class_record) and class_id is not None:
            made: native.ObjectReference = self.session.create_from_class(class_record, class_id, self.stable_id)
            return made
        made = self.session.create(self.TYPE_ID, self.stable_id)
        return made

    @property
    def identity(self) -> int:
        """The object's identity; 0 once released."""
        return self.reference.identity

    def property_info(self, name: str) -> schema.PropertyInfo:
        found: schema.PropertyInfo | None = self.type_info.properties.get(name)
        if found is None:
            raise AttributeError(self.type_info.type_id + " has no property " + name)
        return found

    def get(self, name: str) -> object:
        """The value of the property name."""
        info: schema.PropertyInfo = self.property_info(name)
        value: object = self.session.get_property(self.identity, info.index)
        return value

    def set(self, name: str, value: object) -> None:
        """Sets the property name; an enumeration takes its choice's name ("a, b" for flags) or its value."""
        info: schema.PropertyInfo = self.property_info(name)
        resolver: schema.ChoiceResolver = self.session.schema_cache.resolver(self.type_info, info)
        holder: values.ValueHolder = values.to_gf_value(info.kind, value, resolver)
        self.session.set_property(self.identity, info.index, holder)

    def reset(self, name: str) -> None:
        """Gives the property name back its default."""
        self.property_info(name)
        self.session.reset_property(self.identity, name)

    def connect(self, interaction: str, handler: Handler) -> native.Subscription:
        """Subscribes handler to interaction, one of the type's INTERACTIONS."""
        self.check_interaction(interaction)
        subscription: native.Subscription = self.session.subscribe(self.identity, interaction, handler, False)
        self.subscriptions.append(subscription)
        return subscription

    def check_interaction(self, interaction: str) -> None:
        if len(self.INTERACTIONS) > 0 and interaction not in self.INTERACTIONS:
            raise ValueError(self.TYPE_ID + " has no interaction " + repr(interaction))

    def on(self, interaction: str) -> typing.Callable[[Handler], Handler]:
        """A decorator: ``@button.on("click")`` subscribes the function and returns it unchanged."""
        self.check_interaction(interaction)
        return Subscriber(self, interaction, False)

    def on_change(self, name: str) -> typing.Callable[[Handler], Handler]:
        """A decorator: ``@box.on_change("text")`` subscribes the function to the property's change."""
        self.property_info(name)
        return Subscriber(self, name, True)

    def raise_event(self, interaction: str) -> None:
        """Raises interaction as the library would (C#'s OnClick called directly), through its raiser's base."""
        raiser: Raiser | None = RAISERS.get(interaction)
        if raiser is None:
            raise ValueError("no raiser for " + repr(interaction))
        self.session.check(self.session.raise_hook(self.identity, raiser.class_id, raiser.entry, interaction))

    def dispose(self) -> None:
        """Disposes the object: it leaves its parent and its subscriptions end. The reference stays held."""
        if self.identity != 0:
            self.session.dispose(self.identity)
        self.subscriptions.clear()

    def release(self) -> None:
        """Gives back this object's reference (once)."""
        self.reference.release()

    def __enter__(self) -> Component:
        return self

    def __exit__(self, *unused_exception: object) -> None:
        self.dispose()
        self.release()

    def __repr__(self) -> str:
        return type(self).__name__ + "(" + repr(self.stable_id) + ")"


class Subscriber:
    """The decorator ``on`` and ``on_change`` return: subscribes the function it receives."""

    def __init__(self, component: Component, name: str, property_change: bool) -> None:
        self.component: Component = component
        self.name: str = name
        self.property_change: bool = property_change

    def __call__(self, handler: Handler) -> Handler:
        if self.property_change:
            session: native.Session = self.component.session
            subscription: native.Subscription = session.subscribe(self.component.identity, self.name, handler, True)
            self.component.subscriptions.append(subscription)
            return handler
        self.component.connect(self.name, handler)
        return handler


class Control(Component):
    """A control: a component with a parent, children and layout."""

    __slots__ = ("child_controls",)

    def __init__(self, stable_id: str | None = None, **properties: object) -> None:
        self.child_controls: list[Control] = []
        super().__init__(stable_id, **properties)

    def add(self, *children: Control) -> None:
        """Appends children, in order."""
        for child in children:
            self.session.insert_child(self.identity, child.identity, len(self.child_controls))
            self.child_controls.append(child)

    def remove(self, child: Control) -> None:
        self.session.remove_child(self.identity, child.identity)
        self.child_controls.remove(child)

    @property
    def children(self) -> tuple[Control, ...]:
        return tuple(self.child_controls)

    def focus(self) -> bool:
        """Moves the keyboard focus here; whether it moved."""
        return self.session.focus(self.identity)

    @contextlib.contextmanager
    def layout_suspended(self) -> typing.Iterator[Control]:
        """Suspends layout for the block and lays out once at its end (C#'s SuspendLayout and ResumeLayout)."""
        self.session.suspend_layout(self.identity)
        try:
            yield self
        finally:
            self.session.resume_layout(self.identity, True)

    def dispose(self) -> None:
        super().dispose()
        self.child_controls.clear()
