"""The library's own control schema (GF_TABLE_SCHEMA), read once per type and kept.

The generated classes (``_controls``) carry the schema's names from the
pinned manifest; this module asks the loaded library for what a call needs
at run time: a property's position (properties.get_at and set_at take it),
its kind, its flags and an enumeration's choice values, which the static
manifest does not list. A type is read on first use and kept for the
process; the schema is the same in every call (gf_abi.h, GF_TABLE_SCHEMA).
"""

from __future__ import annotations

import ctypes
import threading

from pyguiforms import _abi
from pyguiforms import values


class Choice:
    """One choice of an enumeration: its name and value."""

    def __init__(self, name: str, value: int) -> None:
        self.name: str = name
        self.value: int = value


class PropertyInfo:
    """One property of a schema type: its position, name, kind, flags and, for an enumeration, its choices."""

    def __init__(self, index: int, name: str, kind: int, flags: int, enumeration: str, choice_count: int) -> None:
        self.index: int = index
        self.name: str = name
        self.kind: int = kind
        self.flags: int = flags
        self.enumeration: str = enumeration
        self.choice_count: int = choice_count
        self.choices: list[Choice] | None = None

    def readable(self) -> bool:
        return (self.flags & _abi.GF_SCHEMA_PROPERTY_FLAGS_READABLE) != 0

    def writable(self) -> bool:
        return (self.flags & _abi.GF_SCHEMA_PROPERTY_FLAGS_WRITABLE) != 0


class TypeInfo:
    """One schema type as the library lists it: its index, its properties and interactions by name."""

    def __init__(self, index: int, type_id: str, type_name: str) -> None:
        self.index: int = index
        self.type_id: str = type_id
        self.type_name: str = type_name
        self.properties: dict[str, PropertyInfo] = {}
        self.interactions: list[str] = []


class ChoiceResolver:
    """Turns a choice name, or flags named "a, b", into an enumeration's value."""

    def __init__(self, cache: SchemaCache, type_info: TypeInfo, property_info: PropertyInfo) -> None:
        self.cache: SchemaCache = cache
        self.type_info: TypeInfo = type_info
        self.property_info: PropertyInfo = property_info

    def __call__(self, name: str) -> int:
        choices: list[Choice] = self.cache.choices(self.type_info, self.property_info)
        combined: int = 0
        for part in name.split(","):
            wanted: str = part.strip()
            found: Choice | None = None
            for choice in choices:
                if choice.name == wanted:
                    found = choice
                    break
            if found is None:
                raise ValueError(self.property_info.name + " has no choice " + repr(wanted) + " (" +
                                 self.property_info.enumeration + ")")
            combined |= found.value
        return combined


class SchemaCache:
    """The types read so far, by the type ID objects.type_id gives. Locked: any thread may look one up."""

    def __init__(self, table: object, check: object) -> None:
        self.table: object = table
        self.check: object = check
        self.lock: threading.Lock = threading.Lock()
        self.types: dict[str, TypeInfo] = {}

    def type_info(self, type_id: str) -> TypeInfo:
        with self.lock:
            found: TypeInfo | None = self.types.get(type_id)
            if found is None:
                found = self.read_type(type_id)
                self.types[type_id] = found
        return found

    def read_type(self, type_id: str) -> TypeInfo:
        encoded: bytes = type_id.encode("utf-8")
        index: ctypes.c_uint64 = ctypes.c_uint64(0)
        self.check(self.table.find_type(values.text_view(encoded), ctypes.byref(index)))
        record: _abi.gf_schema_type = _abi.gf_schema_type()
        record.struct_size = ctypes.sizeof(record)
        self.check(self.table.type_at(index.value, ctypes.byref(record)))
        info: TypeInfo = TypeInfo(index.value, values.read_view(record.id), values.read_view(record.type_name))
        for property_index in range(record.property_count):
            listed: _abi.gf_schema_property = _abi.gf_schema_property()
            listed.struct_size = ctypes.sizeof(listed)
            self.check(self.table.property_at(index.value, property_index, ctypes.byref(listed)))
            name: str = values.read_view(listed.name)
            info.properties[name] = PropertyInfo(property_index, name, listed.kind, listed.flags,
                                                 values.read_view(listed.enumeration), listed.choice_count)
        for interaction_index in range(record.interaction_count):
            interaction: _abi.gf_schema_interaction = _abi.gf_schema_interaction()
            interaction.struct_size = ctypes.sizeof(interaction)
            self.check(self.table.interaction_at(index.value, interaction_index, ctypes.byref(interaction)))
            info.interactions.append(values.read_view(interaction.name))
        return info

    def choices(self, type_info: TypeInfo, property_info: PropertyInfo) -> list[Choice]:
        with self.lock:
            if property_info.choices is None:
                read: list[Choice] = []
                for choice_index in range(property_info.choice_count):
                    record: _abi.gf_schema_choice = _abi.gf_schema_choice()
                    record.struct_size = ctypes.sizeof(record)
                    self.check(self.table.choice_at(type_info.index, property_info.index, choice_index,
                                                    ctypes.byref(record)))
                    read.append(Choice(values.read_view(record.name), record.value))
                property_info.choices = read
            found: list[Choice] = property_info.choices
        return found

    def resolver(self, type_info: TypeInfo, property_info: PropertyInfo) -> ChoiceResolver:
        resolver: ChoiceResolver = ChoiceResolver(self, type_info, property_info)
        return resolver
