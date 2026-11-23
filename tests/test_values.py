"""Python values round-trip through gf_value without the library."""

from __future__ import annotations

import unittest

from pyguiforms import _abi
from pyguiforms import values


class ChoiceTable:
    """A stand-in for the schema's choices: "left" 1, "right" 2."""

    def __call__(self, name: str) -> int:
        table: dict[str, int] = {"left": 1, "right": 2}
        return table[name]


def round_trip(kind: int, value: object) -> object:
    holder: values.ValueHolder = values.to_gf_value(kind, value, ChoiceTable())
    copied: object = values.from_gf_value(holder.value)
    return copied


class ValueTests(unittest.TestCase):

    def test_scalars(self) -> None:
        self.assertIs(round_trip(_abi.GF_VALUE_KIND_BOOLEAN, True), True)
        self.assertEqual(round_trip(_abi.GF_VALUE_KIND_SIGNED, -7), -7)
        self.assertEqual(round_trip(_abi.GF_VALUE_KIND_UNSIGNED, 7), 7)
        self.assertEqual(round_trip(_abi.GF_VALUE_KIND_NUMBER, 2.5), 2.5)
        self.assertEqual(round_trip(_abi.GF_VALUE_KIND_TEXT, "héllo"), "héllo")
        self.assertEqual(round_trip(_abi.GF_VALUE_KIND_COLOR, values.rgba(1, 2, 3)), 0x010203FF)

    def test_geometry_accepts_tuples(self) -> None:
        self.assertEqual(round_trip(_abi.GF_VALUE_KIND_POINT, (1, 2)), values.Point(1.0, 2.0))
        self.assertEqual(round_trip(_abi.GF_VALUE_KIND_SIZE, values.Size(3, 4)), values.Size(3.0, 4.0))
        self.assertEqual(round_trip(_abi.GF_VALUE_KIND_RECTANGLE, (1, 2, 3, 4)), values.Rect(1.0, 2.0, 3.0, 4.0))
        self.assertEqual(round_trip(_abi.GF_VALUE_KIND_INSETS, (1, 2, 3, 4)), values.Insets(1.0, 2.0, 3.0, 4.0))

    def test_font(self) -> None:
        font: values.Font = values.Font(_abi.GF_FONT_ROLE_BODY if hasattr(_abi, "GF_FONT_ROLE_BODY") else 0,
                                        weight=700, size=14.0)
        copied: object = round_trip(_abi.GF_VALUE_KIND_FONT, font)
        self.assertEqual(copied, font)

    def test_enumeration_by_name_is_passed_by_value(self) -> None:
        holder: values.ValueHolder = values.to_gf_value(_abi.GF_VALUE_KIND_ENUMERATION, "right", ChoiceTable())
        self.assertEqual(holder.value.signed_integer, 2)
        # A value the caller passes carries no name: it reads back as its value.
        self.assertEqual(values.from_gf_value(holder.value), 2)

    def test_null(self) -> None:
        self.assertIsNone(round_trip(_abi.GF_VALUE_KIND_TEXT, None))

    def test_out_of_range_colors_are_refused(self) -> None:
        with self.assertRaises(ValueError):
            values.rgba(256, 0, 0)


if __name__ == "__main__":
    unittest.main()
