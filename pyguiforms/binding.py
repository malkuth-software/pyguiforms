"""Model values a form document binds (``<bind property="checked" to="autosave"/>``).

A ``Value`` holds one value and tells its observers when it changes, as
GUI.Forms' C++ ``Value<T>`` does. A model is any Python object whose
attributes are ``Value`` objects; the form loader finds each ``to`` by
attribute name. A binding sets the property from the value when the
control is made and whenever the value changes; a two-way binding also
writes the property's changes back.

A ``Value`` is used on the UI thread, as the controls it is bound to are:
its observers run in ``set``'s caller.
"""

from __future__ import annotations

import typing

Observer = typing.Callable[[object], None]


class Observation:
    """One observer of a Value, ended once by ``end``."""

    def __init__(self, source: Value, observer: Observer) -> None:
        self.source: Value | None = source
        self.observer: Observer = observer

    def end(self) -> None:
        source: Value | None = self.source
        self.source = None
        if source is not None:
            source.observations.remove(self)


class Value:
    """One observable value of a model."""

    def __init__(self, initial: object = None) -> None:
        self.current: object = initial
        self.observations: list[Observation] = []
        self.notifying: bool = False

    @property
    def value(self) -> object:
        return self.current

    @value.setter
    def value(self, new_value: object) -> None:
        self.set(new_value)

    def set(self, new_value: object) -> None:
        """Changes the value and tells every observer, unless it is equal or this is a nested change."""
        if new_value == self.current:
            return
        self.current = new_value
        if self.notifying:
            return
        self.notifying = True
        try:
            for observation in tuple(self.observations):
                observation.observer(new_value)
        finally:
            self.notifying = False

    def observe(self, observer: Observer) -> Observation:
        observation: Observation = Observation(self, observer)
        self.observations.append(observation)
        return observation

    def __repr__(self) -> str:
        return "Value(" + repr(self.current) + ")"


class PropertyWriter:
    """An observer that writes a Value's changes into one control property."""

    def __init__(self, control: object, name: str) -> None:
        self.control: object = control
        self.name: str = name

    def __call__(self, new_value: object) -> None:
        self.control.set(self.name, new_value)


class ValueWriter:
    """A property-change handler that writes the control's property back into a Value (two-way)."""

    def __init__(self, control: object, name: str, source: Value) -> None:
        self.control: object = control
        self.name: str = name
        self.source: Value = source

    def __call__(self, event: object) -> None:
        self.source.set(self.control.get(self.name))
