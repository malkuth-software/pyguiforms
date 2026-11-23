"""The application's theme (GF_TABLE_THEMES): CSS theme sheets, published values and images.

    pyguiforms.themes.load_sheet(pathlib.Path("app.theme.css").read_text(), "app")

The library holds one theme for every window it shows: a sheet loaded
before ``run`` is the window's from its first frame, and one loaded during
a run replaces the running window's at once. A form document names roles
with ``classes``; the sheet gives each role its look (gui_forms
docs/user/themes.md and theme-language.md). A refused sheet changes
nothing and raises ``ThemeError`` with each finding's code, line and
column; a sheet that loads with warnings returns them. UI thread only.
"""

from __future__ import annotations

import ctypes

from pyguiforms import _abi
from pyguiforms import native
from pyguiforms import values


class Finding:
    """One finding of a load: severity ("error" or "warning"), code, name, file, place, rule, property, detail."""

    def __init__(self, severity: str, line: int, column: int, texts: dict[str, str]) -> None:
        self.severity: str = severity
        self.line: int = line
        self.column: int = column
        self.code: str = texts["code"]
        self.name: str = texts["name"]
        self.file: str = texts["file"]
        self.rule: str = texts["rule"]
        self.property_name: str = texts["property"]
        self.detail: str = texts["detail"]

    def __str__(self) -> str:
        text: str = self.file + ":" + str(self.line) + ":" + str(self.column) + ": " + self.severity + " " + \
            self.code + " " + self.name
        if self.detail != "":
            text += ": " + self.detail
        return text


class ThemeError(Exception):
    """A refused sheet: its findings. The theme in use is unchanged."""

    def __init__(self, findings: list[Finding]) -> None:
        lines: list[str] = []
        for finding in findings:
            lines.append(str(finding))
        super().__init__("the theme is refused:\n" + "\n".join(lines))
        self.findings: list[Finding] = findings


TEXTS: tuple[tuple[str, int], ...] = (
    ("code", _abi.GF_THEME_DIAGNOSTIC_TEXT_CODE),
    ("name", _abi.GF_THEME_DIAGNOSTIC_TEXT_NAME),
    ("file", _abi.GF_THEME_DIAGNOSTIC_TEXT_FILE),
    ("rule", _abi.GF_THEME_DIAGNOSTIC_TEXT_RULE),
    ("property", _abi.GF_THEME_DIAGNOSTIC_TEXT_PROPERTY),
    ("detail", _abi.GF_THEME_DIAGNOSTIC_TEXT_DETAIL),
)


class FindingTextCall:
    """A named target for native.read_text_slot: one finding's text."""

    def __init__(self, table: native.Table, index: int, text: int) -> None:
        self.table: native.Table = table
        self.index: int = index
        self.text: int = text

    def __call__(self, buffer: object, capacity: int, required: object) -> int:
        status: int = self.table.diagnostic_text(self.index, self.text, buffer, capacity, required)
        return status


def table() -> native.Table:
    session: native.Session = native.session()
    session.require_ui_thread()
    themes: native.Table = session.library.table("gf_themes_table")
    return themes


def findings(count: int) -> list[Finding]:
    """The findings the last load or install holds, in the compiler's order."""
    themes: native.Table = table()
    library: native.Library = native.session().library
    read: list[Finding] = []
    for index in range(count):
        record: _abi.gf_theme_diagnostic = _abi.gf_theme_diagnostic()
        record.struct_size = ctypes.sizeof(record)
        library.check(themes.diagnostic_at(index, ctypes.byref(record)))
        texts: dict[str, str] = {}
        for name, text in TEXTS:
            texts[name] = native.read_text_slot(library, FindingTextCall(themes, index, text))
        severity: str = "error" if record.severity == _abi.GF_THEME_SEVERITY_ERROR else "warning"
        read.append(Finding(severity, record.line, record.column, texts))
    return read


def load_sheet(sheet: str, name: str) -> list[Finding]:
    """Makes the CSS sheet (its text) the theme, named name; returns its warnings, raises ThemeError if refused."""
    themes: native.Table = table()
    library: native.Library = native.session().library
    sheet_bytes: bytes = sheet.encode("utf-8")
    name_bytes: bytes = name.encode("utf-8")
    report: _abi.gf_theme_report = _abi.gf_theme_report()
    report.struct_size = ctypes.sizeof(report)
    status: int = themes.load_sheet(values.text_view(sheet_bytes), values.text_view(name_bytes),
                                    ctypes.byref(report))
    library.check(status)
    found: list[Finding] = findings(report.diagnostic_count)
    if report.outcome != _abi.GF_THEME_OUTCOME_APPLIED:
        raise ThemeError(found)
    return found


def reset() -> None:
    """Makes the built-in theme the theme again."""
    themes: native.Table = table()
    native.session().library.check(themes.reset())


def theme_id() -> str:
    """The id of the theme in use (the name it was loaded under)."""
    themes: native.Table = table()
    text: str = native.read_text_slot(native.session().library, themes.theme_id)
    return text


def publish_value(name: str, value: float) -> None:
    """Publishes a value sheets read as var(--name); open windows repaint what reads it."""
    themes: native.Table = table()
    name_bytes: bytes = name.encode("utf-8")
    native.session().library.check(themes.publish_value(values.text_view(name_bytes), float(value)))


def withdraw_value(name: str) -> None:
    themes: native.Table = table()
    name_bytes: bytes = name.encode("utf-8")
    native.session().library.check(themes.withdraw_value(values.text_view(name_bytes)))


def published_value(name: str) -> float | None:
    """The published value of name, or None when it is not published."""
    themes: native.Table = table()
    name_bytes: bytes = name.encode("utf-8")
    value: ctypes.c_double = ctypes.c_double(0.0)
    present: ctypes.c_uint32 = ctypes.c_uint32(0)
    native.session().library.check(themes.published_value(values.text_view(name_bytes), ctypes.byref(value),
                                                          ctypes.byref(present)))
    if present.value == 0:
        return None
    return value.value


def load_image(png: bytes) -> int:
    """Admits a PNG into the image registry; returns the id an IMAGE property takes."""
    themes: native.Table = table()
    data: ctypes.Array = (ctypes.c_uint8 * len(png)).from_buffer_copy(png)
    image: ctypes.c_uint64 = ctypes.c_uint64(0)
    native.session().library.check(themes.load_image(data, len(png), ctypes.byref(image)))
    return image.value


def remove_image(image: int) -> None:
    themes: native.Table = table()
    native.session().library.check(themes.remove_image(image))
