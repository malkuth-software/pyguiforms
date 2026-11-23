"""Python values and their ``gf_value`` form (gf_abi.h, gf_value).

A property or event value crosses the ABI as a ``gf_value``: ``kind``
selects the field that holds it. This module converts both ways:

| Kind | Python value |
|---|---|
| BOOLEAN | ``bool`` |
| SIGNED, UNSIGNED | ``int`` |
| NUMBER | ``float`` (an ``int`` is accepted) |
| TEXT | ``str`` |
| POINT, SIZE, RECTANGLE, INSETS | ``Point``, ``Size``, ``Rect``, ``Insets`` (a plain tuple is accepted) |
| COLOR | ``int`` 0xRRGGBBAA, not premultiplied (``rgba`` makes one) |
| FONT | ``Font`` |
| IMAGE | ``int``, an image id (0 is none) |
| ENUMERATION | ``str``, the choice's name ("top, left" for flags); a value is set by name or ``int`` |
| COLLECTION | ``list`` of the item values |
| NULL | ``None`` |

Lifetime: ``ValueHolder`` owns everything a ``gf_value`` it built points at
(the encoded text, a collection's element array), so the value is valid
while the holder lives; the library copies what it keeps during the call.
A value the library lends (an event field, a property read) is copied out
by ``from_gf_value`` before the call or the invoke ends.
"""

from __future__ import annotations

import ctypes
import typing

from pyguiforms import _abi


class Point(typing.NamedTuple):
    x: float
    y: float


class Size(typing.NamedTuple):
    width: float
    height: float


class Rect(typing.NamedTuple):
    x: float
    y: float
    width: float
    height: float


class Insets(typing.NamedTuple):
    left: float
    top: float
    right: float
    bottom: float


class Font(typing.NamedTuple):
    """A font (gf_font): role (GF_FONT_ROLE_*), weight 1 to 1000, italic, size and letter spacing in logical pixels.

    ``reserved`` is the font's bundled family and family stack word, read
    from a font and passed back within one process (gf_abi.h, gf_font).
    """

    role: int = _abi.GF_FONT_ROLE_CONTROL
    weight: int = 400
    italic: bool = False
    size: float = 12.0
    letter_spacing: float = 0.0
    reserved: int = 0


def rgba(red: int, green: int, blue: int, alpha: int = 255) -> int:
    """A colour as the ABI writes it: 0xRRGGBBAA, red in the high byte, not premultiplied."""
    for component in (red, green, blue, alpha):
        if component < 0 or component > 255:
            raise ValueError("a colour component is from 0 to 255, not " + str(component))
    packed: int = (red << 24) | (green << 16) | (blue << 8) | alpha
    return packed


KIND_NAMES: dict[str, int] = {
    "null": _abi.GF_VALUE_KIND_NULL,
    "boolean": _abi.GF_VALUE_KIND_BOOLEAN,
    "signed_integer": _abi.GF_VALUE_KIND_SIGNED,
    "unsigned_integer": _abi.GF_VALUE_KIND_UNSIGNED,
    "number": _abi.GF_VALUE_KIND_NUMBER,
    "text": _abi.GF_VALUE_KIND_TEXT,
    "point": _abi.GF_VALUE_KIND_POINT,
    "size": _abi.GF_VALUE_KIND_SIZE,
    "rectangle": _abi.GF_VALUE_KIND_RECTANGLE,
    "insets": _abi.GF_VALUE_KIND_INSETS,
    "color": _abi.GF_VALUE_KIND_COLOR,
    "font": _abi.GF_VALUE_KIND_FONT,
    "image": _abi.GF_VALUE_KIND_IMAGE,
    "enumeration": _abi.GF_VALUE_KIND_ENUMERATION,
    "object": _abi.GF_VALUE_KIND_OBJECT,
    "collection": _abi.GF_VALUE_KIND_COLLECTION,
}

# A collection the caller passes holds at most this many elements (gf_abi.h, N16).
MAXIMUM_COLLECTION_ELEMENTS: int = 4096


def text_view(encoded: bytes) -> _abi.gf_utf8_view:
    """A view of encoded; the caller keeps encoded alive while the view is used."""
    view: _abi.gf_utf8_view = _abi.gf_utf8_view()
    view.data = ctypes.cast(ctypes.c_char_p(encoded), ctypes.POINTER(ctypes.c_char))
    view.size = len(encoded)
    return view


def read_view(view: _abi.gf_utf8_view) -> str:
    """Copies a lent view's text out (an empty view may have a null data pointer)."""
    if view.size == 0:
        return ""
    copied: bytes = ctypes.string_at(view.data, view.size)
    return copied.decode("utf-8")


class ValueHolder:
    """A gf_value built from a Python value, and the storage it points at."""

    def __init__(self) -> None:
        self.value: _abi.gf_value = _abi.gf_value()
        self.value.struct_size = ctypes.sizeof(_abi.gf_value)
        self.kept: list[object] = []

    def reference(self) -> object:
        return ctypes.byref(self.value)


def as_float_pair(value: object, what: str) -> tuple[float, float]:
    items: tuple = tuple(value)
    if len(items) != 2:
        raise ValueError(what + " has two numbers, not " + repr(value))
    pair: tuple[float, float] = (float(items[0]), float(items[1]))
    return pair


def as_float_quad(value: object, what: str) -> tuple[float, float, float, float]:
    items: tuple = tuple(value)
    if len(items) != 4:
        raise ValueError(what + " has four numbers, not " + repr(value))
    quad: tuple[float, float, float, float] = (float(items[0]), float(items[1]), float(items[2]), float(items[3]))
    return quad


def fill_value(record: _abi.gf_value, kind: int, value: object, holder: ValueHolder,
               choice_value: typing.Callable[[str], int] | None) -> None:
    """Writes value into record as kind; holder keeps what record points at.

    choice_value turns an ENUMERATION's choice name into its value (the
    schema's choices); without it an enumeration takes an int only.
    """
    record.struct_size = ctypes.sizeof(_abi.gf_value)
    record.kind = kind
    if value is None:
        record.kind = _abi.GF_VALUE_KIND_NULL
        return
    if kind == _abi.GF_VALUE_KIND_BOOLEAN:
        record.boolean = 1 if bool(value) else 0
        return
    if kind == _abi.GF_VALUE_KIND_SIGNED:
        record.signed_integer = int(value)
        return
    if kind == _abi.GF_VALUE_KIND_UNSIGNED or kind == _abi.GF_VALUE_KIND_IMAGE:
        if int(value) < 0:
            raise ValueError("an unsigned value cannot be negative: " + repr(value))
        record.unsigned_integer = int(value)
        return
    if kind == _abi.GF_VALUE_KIND_NUMBER:
        record.number = float(value)
        return
    if kind == _abi.GF_VALUE_KIND_TEXT:
        if not isinstance(value, str):
            raise TypeError("a text value is a str, not " + type(value).__name__)
        encoded: bytes = value.encode("utf-8")
        holder.kept.append(encoded)
        record.text = text_view(encoded)
        return
    if kind == _abi.GF_VALUE_KIND_POINT:
        x, y = as_float_pair(value, "a point")
        record.point.x = x
        record.point.y = y
        return
    if kind == _abi.GF_VALUE_KIND_SIZE:
        width, height = as_float_pair(value, "a size")
        record.size.width = width
        record.size.height = height
        return
    if kind == _abi.GF_VALUE_KIND_RECTANGLE:
        rx, ry, rwidth, rheight = as_float_quad(value, "a rectangle")
        record.rectangle.x = rx
        record.rectangle.y = ry
        record.rectangle.width = rwidth
        record.rectangle.height = rheight
        return
    if kind == _abi.GF_VALUE_KIND_INSETS:
        left, top, right, bottom = as_float_quad(value, "insets")
        record.insets.left = left
        record.insets.top = top
        record.insets.right = right
        record.insets.bottom = bottom
        return
    if kind == _abi.GF_VALUE_KIND_COLOR:
        colour: int = int(value)
        if colour < 0 or colour > 0xFFFFFFFF:
            raise ValueError("a colour is 0xRRGGBBAA, not " + repr(value))
        record.color = colour
        return
    if kind == _abi.GF_VALUE_KIND_FONT:
        font: Font = value if isinstance(value, Font) else Font(*tuple(value))
        record.font.role = font.role
        record.font.weight = font.weight
        record.font.italic = 1 if font.italic else 0
        record.font.reserved = font.reserved
        record.font.size = font.size
        record.font.letter_spacing = font.letter_spacing
        return
    if kind == _abi.GF_VALUE_KIND_ENUMERATION:
        if isinstance(value, str):
            if choice_value is None:
                raise TypeError("this enumeration takes an int; its choices are not known here")
            record.signed_integer = choice_value(value)
            return
        record.signed_integer = int(value)
        return
    if kind == _abi.GF_VALUE_KIND_COLLECTION:
        fill_collection(record, value, holder)
        return
    raise TypeError("no gf_value form for kind " + str(kind))


def element_kind(item: object) -> int:
    """The kind of one element of a collection the caller passes, from its Python type."""
    if isinstance(item, bool):
        return _abi.GF_VALUE_KIND_BOOLEAN
    if isinstance(item, int):
        return _abi.GF_VALUE_KIND_SIGNED
    if isinstance(item, float):
        return _abi.GF_VALUE_KIND_NUMBER
    if isinstance(item, str):
        return _abi.GF_VALUE_KIND_TEXT
    if isinstance(item, Point):
        return _abi.GF_VALUE_KIND_POINT
    if isinstance(item, Size):
        return _abi.GF_VALUE_KIND_SIZE
    if isinstance(item, Rect):
        return _abi.GF_VALUE_KIND_RECTANGLE
    if isinstance(item, Insets):
        return _abi.GF_VALUE_KIND_INSETS
    if isinstance(item, Font):
        return _abi.GF_VALUE_KIND_FONT
    raise TypeError("no collection element form for " + type(item).__name__)


def fill_collection(record: _abi.gf_value, value: object, holder: ValueHolder) -> None:
    items: list = list(value)
    if len(items) > MAXIMUM_COLLECTION_ELEMENTS:
        raise ValueError("a collection passes at most " + str(MAXIMUM_COLLECTION_ELEMENTS) + " elements, not " +
                         str(len(items)))
    record.element_count = len(items)
    if len(items) == 0:
        return
    elements: ctypes.Array = (_abi.gf_value * len(items))()
    holder.kept.append(elements)
    for index in range(len(items)):
        fill_value(elements[index], element_kind(items[index]), items[index], holder, None)
    record.elements = ctypes.cast(elements, ctypes.POINTER(_abi.gf_value))


def to_gf_value(kind: int, value: object, choice_value: typing.Callable[[str], int] | None = None) -> ValueHolder:
    holder: ValueHolder = ValueHolder()
    fill_value(holder.value, kind, value, holder, choice_value)
    return holder


def from_gf_value(record: _abi.gf_value) -> object:
    """Copies a gf_value out as its Python value. A COLLECTION gives its element count (read elements apart)."""
    kind: int = record.kind
    if kind == _abi.GF_VALUE_KIND_NULL:
        return None
    if kind == _abi.GF_VALUE_KIND_BOOLEAN:
        return record.boolean != 0
    if kind == _abi.GF_VALUE_KIND_SIGNED:
        return record.signed_integer
    if kind == _abi.GF_VALUE_KIND_UNSIGNED or kind == _abi.GF_VALUE_KIND_IMAGE:
        return record.unsigned_integer
    if kind == _abi.GF_VALUE_KIND_OBJECT:
        return record.unsigned_integer
    if kind == _abi.GF_VALUE_KIND_NUMBER:
        return record.number
    if kind == _abi.GF_VALUE_KIND_TEXT:
        return read_view(record.text)
    if kind == _abi.GF_VALUE_KIND_POINT:
        return Point(record.point.x, record.point.y)
    if kind == _abi.GF_VALUE_KIND_SIZE:
        return Size(record.size.width, record.size.height)
    if kind == _abi.GF_VALUE_KIND_RECTANGLE:
        return Rect(record.rectangle.x, record.rectangle.y, record.rectangle.width, record.rectangle.height)
    if kind == _abi.GF_VALUE_KIND_INSETS:
        return Insets(record.insets.left, record.insets.top, record.insets.right, record.insets.bottom)
    if kind == _abi.GF_VALUE_KIND_COLOR:
        return record.color
    if kind == _abi.GF_VALUE_KIND_FONT:
        return Font(record.font.role, record.font.weight, record.font.italic != 0, record.font.size,
                    record.font.letter_spacing, record.font.reserved)
    if kind == _abi.GF_VALUE_KIND_ENUMERATION:
        # The library names the choice; an unknown value comes with empty text.
        name: str = read_view(record.text)
        if name == "":
            return record.signed_integer
        return name
    if kind == _abi.GF_VALUE_KIND_COLLECTION:
        return record.unsigned_integer
    raise TypeError("unknown gf_value kind " + str(kind))
