#!/usr/bin/env python3
"""Generates pyguiforms' 1:1 layer from GUI.Forms' audited ABI manifest.

The manifest (gui_forms ``manifests/abi/gf_abi.json``, written by
``tools/abi_audit.py extract``) is the only input: every type, field offset,
slot signature and constant comes from it, as for the C# and C++ targets of
gui_forms ``tools/abi_bindings.py``. This is the study's prototype of a third
target; STUDY.md recommends where it lives.

Two outputs:

- ``python`` writes ``pyguiforms/_abi.py``: every scalar typedef as its ctypes
  fixed-width type, every record, extensible record, segment, class table and
  function table as a ``ctypes.Structure`` whose fields are the C fields in
  order (slots as ``CFUNCTYPE`` types), every constant as an ``int``, the one
  export's prototype, the table ids by table, and ``LAYOUT`` with
  ``check_layout()``, which compares every size and field offset ctypes lays
  out with the manifest's numbers, so an import on any host proves its own
  layout (the C# ``Layout.check``).
- ``cdef`` writes the same declarations as C for cffi's ``ffi.cdef`` (the
  study's benchmark of cffi's ABI and API modes).

``--check`` fails when a written file differs from what the manifest gives.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST: pathlib.Path = ROOT.parent / "gui_forms" / "manifests" / "abi" / "gf_abi.json"
PYTHON_OUTPUT: pathlib.Path = ROOT / "pyguiforms" / "_abi.py"
CDEF_OUTPUT: pathlib.Path = ROOT / "bench" / "gf_abi_cdef.h"

# The C fixed-width types the ABI's dialect admits, as ctypes types.
PRIMITIVES: dict[str, str] = {
    "uint8_t": "ctypes.c_uint8",
    "int8_t": "ctypes.c_int8",
    "uint16_t": "ctypes.c_uint16",
    "int16_t": "ctypes.c_int16",
    "uint32_t": "ctypes.c_uint32",
    "int32_t": "ctypes.c_int32",
    "uint64_t": "ctypes.c_uint64",
    "int64_t": "ctypes.c_int64",
    "double": "ctypes.c_double",
    "float": "ctypes.c_float",
    "char": "ctypes.c_char",
}


class ParsedType:
    """A manifest type spelling taken apart: its base name, pointer depth and array length."""

    def __init__(self, base: str, pointer_depth: int, array_length: int) -> None:
        self.base: str = base
        self.pointer_depth: int = pointer_depth
        self.array_length: int = array_length


def parse_type(spelling: str) -> ParsedType:
    text: str = spelling.strip()
    array_length: int = 0
    if text.endswith("]"):
        open_bracket: int = text.index("[")
        array_length = int(text[open_bracket + 1:-1])
        text = text[:open_bracket]
    if text.startswith("const "):
        text = text[len("const "):]
    if text.startswith("struct "):
        text = text[len("struct "):]
    pointer_depth: int = 0
    while text.endswith("*"):
        pointer_depth += 1
        text = text[:-1].strip()
    parsed: ParsedType = ParsedType(text, pointer_depth, array_length)
    return parsed


class Names:
    """The manifest's named types, by kind, for resolving a spelling."""

    def __init__(self, manifest: dict) -> None:
        self.scalars: dict[str, str] = {}
        for scalar in manifest["scalars"]:
            self.scalars[scalar["name"]] = scalar["type"]
        self.callbacks: set[str] = set()
        for callback in manifest["callbacks"]:
            self.callbacks.add(callback["name"])
        self.structs: set[str] = set()
        for struct in manifest["structs"]:
            self.structs.add(struct["name"])


# ---------------------------------------------------------------- ctypes target


def ctypes_value_type(base: str, names: Names) -> str:
    """The ctypes type of a non-pointer base name."""
    if base in PRIMITIVES:
        return PRIMITIVES[base]
    if base in names.scalars:
        return base
    if base in names.structs or base in names.callbacks:
        return base
    raise SystemExit("abi_python: unknown type " + base)


def ctypes_type(spelling: str, names: Names) -> str:
    parsed: ParsedType = parse_type(spelling)
    if parsed.base == "void" and parsed.pointer_depth == 0:
        return "None"
    result: str = ""
    if parsed.pointer_depth == 0:
        result = ctypes_value_type(parsed.base, names)
    elif parsed.base == "void" and parsed.pointer_depth == 1:
        result = "ctypes.c_void_p"
    else:
        # char* stays POINTER(c_char), not c_char_p: ABI text is a view with a
        # size and is never terminated, so the hand-written layer reads it
        # with ctypes.string_at(data, size).
        result = ctypes_value_type(parsed.base, names)
        depth: int = parsed.pointer_depth
        if parsed.base == "void":
            result = "ctypes.c_void_p"
            depth -= 1
        for unused_level in range(depth):
            result = "ctypes.POINTER(" + result + ")"
    if parsed.array_length > 0:
        result = "(" + result + " * " + str(parsed.array_length) + ")"
    return result


def ctypes_function_type(signature: dict, names: Names) -> str:
    arguments: list[str] = [ctypes_type(signature["returns"], names)]
    for parameter in signature["parameters"]:
        arguments.append(ctypes_type(parameter["type"], names))
    joined: str = ", ".join(arguments)
    return "ctypes.CFUNCTYPE(" + joined + ")"


def table_ids(manifest: dict) -> list[tuple[str, str]]:
    """Each function table and its GF_TABLE_* constant (gf_<name>_table: GF_TABLE_<NAME>)."""
    constants: set[str] = set()
    for constant in manifest["constants"]:
        constants.add(constant["name"])
    pairs: list[tuple[str, str]] = []
    for struct in manifest["structs"]:
        if struct["kind"] != "table":
            continue
        stem: str = struct["name"][len("gf_"):-len("_table")]
        constant_name: str = "GF_TABLE_" + stem.upper()
        if constant_name not in constants:
            raise SystemExit("abi_python: table " + struct["name"] + " has no " + constant_name)
        pairs.append((struct["name"], constant_name))
    return pairs


def render_python(manifest: dict) -> str:
    names: Names = Names(manifest)
    abi: dict = manifest["abi"]
    lines: list[str] = []
    lines.append("# Generated from gui_forms manifests/abi/gf_abi.json by `python3 tools/abi_python.py python`.")
    lines.append("# Do not edit. The 1:1 layer: names, layouts and slot types exactly as the C header has them.")
    lines.append("")
    lines.append("import ctypes")
    lines.append("")
    lines.append("ABI_MAJOR = " + str(abi["major"]))
    lines.append("ABI_MINOR = " + str(abi["minor"]))
    lines.append("")
    lines.append("# Scalar typedefs.")
    for scalar in manifest["scalars"]:
        lines.append(scalar["name"] + " = " + PRIMITIVES[scalar["type"]])
    lines.append("")
    lines.append("# Constants.")
    for constant in manifest["constants"]:
        lines.append(constant["name"] + " = " + str(constant["value"]))
    lines.append("")
    lines.append("# Records and tables, declared first so that fields and slots may name any of them.")
    for struct in manifest["structs"]:
        lines.append("")
        lines.append("")
        lines.append("class " + struct["name"] + "(ctypes.Structure):")
        lines.append("    \"\"\"" + struct["name"] + " (" + struct["kind"] + ", " + str(struct["size"]) + " bytes).\"\"\"")
    lines.append("")
    lines.append("")
    lines.append("# Callback typedefs.")
    for callback in manifest["callbacks"]:
        lines.append(callback["name"] + " = " + ctypes_function_type(callback, names))
    lines.append("")
    lines.append("# Fields, in C order.")
    for struct in manifest["structs"]:
        lines.append(struct["name"] + "._fields_ = [")
        for field in struct["fields"]:
            field_type: str = ""
            if field["type"] == "function":
                field_type = ctypes_function_type(field["signature"], names)
            else:
                field_type = ctypes_type(field["type"], names)
            lines.append("    (\"" + field["name"] + "\", " + field_type + "),")
        lines.append("]")
    lines.append("")
    lines.append("# The one export, bound to a loaded library by bind_exports.")
    for export in manifest["exports"]:
        lines.append("")
        lines.append("")
        lines.append("def bind_" + export["name"] + "(library):")
        lines.append("    function = library." + export["name"])
        lines.append("    function.restype = " + ctypes_type(export["returns"], names))
        argument_types: list[str] = []
        for parameter in export["parameters"]:
            argument_types.append(ctypes_type(parameter["type"], names))
        lines.append("    function.argtypes = [" + ", ".join(argument_types) + "]")
        lines.append("    return function")
    lines.append("")
    lines.append("")
    lines.append("# Each function table's id for gf_abi_get_table.")
    lines.append("TABLE_IDS = {")
    for table_name, constant_name in table_ids(manifest):
        lines.append("    \"" + table_name + "\": " + constant_name + ",")
    lines.append("}")
    lines.append("")
    lines.append("# The manifest's size and field offsets of every record, for check_layout.")
    lines.append("LAYOUT = {")
    for struct in manifest["structs"]:
        offsets: list[str] = []
        for field in struct["fields"]:
            offsets.append("(\"" + field["name"] + "\", " + str(field["offset"]) + ")")
        lines.append("    \"" + struct["name"] + "\": (" + str(struct["size"]) + ", (" + ", ".join(offsets) + ",)),")
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def check_layout():")
    lines.append("    \"\"\"The records whose ctypes size or field offsets differ from the manifest's, as messages.\"\"\"")
    lines.append("    mismatches = []")
    lines.append("    module = globals()")
    lines.append("    for name in LAYOUT:")
    lines.append("        size, offsets = LAYOUT[name]")
    lines.append("        record = module[name]")
    lines.append("        if ctypes.sizeof(record) != size:")
    lines.append("            mismatches.append(name + \": size \" + str(ctypes.sizeof(record)) + \", manifest \" + str(size))")
    lines.append("        for field_name, offset in offsets:")
    lines.append("            laid_out = getattr(record, field_name).offset")
    lines.append("            if laid_out != offset:")
    lines.append("                mismatches.append(name + \".\" + field_name + \": offset \" + str(laid_out) + \", manifest \" + str(offset))")
    lines.append("    return mismatches")
    lines.append("")
    text: str = "\n".join(lines)
    return text


# ------------------------------------------------------------------ cdef target


def c_declarator(spelling: str, name: str) -> str:
    parsed: ParsedType = parse_type(spelling)
    if parsed.array_length > 0:
        element: str = spelling[:spelling.index("[")]
        return element + " " + name + "[" + str(parsed.array_length) + "]"
    return spelling + " " + name


def c_function_pointer(signature: dict, name: str) -> str:
    parameters: list[str] = []
    for parameter in signature["parameters"]:
        parameters.append(c_declarator(parameter["type"], parameter["name"]))
    if len(parameters) == 0:
        parameters.append("void")
    return signature["returns"] + " (*" + name + ")(" + ", ".join(parameters) + ")"


def render_cdef(manifest: dict) -> str:
    lines: list[str] = []
    lines.append("/* Generated from gui_forms manifests/abi/gf_abi.json by `python3 tools/abi_python.py cdef`. Do not edit. */")
    for scalar in manifest["scalars"]:
        lines.append("typedef " + scalar["type"] + " " + scalar["name"] + ";")
    suffixes: dict[str, str] = {"uint32": "u", "uint64": "ull", "int32": ""}
    for constant in manifest["constants"]:
        lines.append("#define " + constant["name"] + " " + str(constant["value"]) + suffixes[constant["type"]])
    for struct in manifest["structs"]:
        lines.append("typedef struct " + struct["name"] + " " + struct["name"] + ";")
    for callback in manifest["callbacks"]:
        lines.append("typedef " + c_function_pointer(callback, callback["name"]) + ";")
    for struct in manifest["structs"]:
        lines.append("struct " + struct["name"] + " {")
        for field in struct["fields"]:
            if field["type"] == "function":
                lines.append("    " + c_function_pointer(field["signature"], field["name"]) + ";")
            else:
                lines.append("    " + c_declarator(field["type"], field["name"]) + ";")
        lines.append("};")
    for export in manifest["exports"]:
        lines.append(c_function_pointer(export, export["name"]).replace("(*" + export["name"] + ")", export["name"]) + ";")
    lines.append("")
    text: str = "\n".join(lines)
    return text


# ------------------------------------------------------------------------- main


def write_or_check(text: str, output: pathlib.Path, check: bool) -> int:
    if check:
        if not output.exists() or output.read_text(encoding="utf-8") != text:
            print("abi_python: " + str(output) + " differs from the manifest", file=sys.stderr)
            return 1
        return 0
    output.write_text(text, encoding="utf-8")
    return 0


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target", choices=["python", "cdef"])
    parser.add_argument("--manifest", type=pathlib.Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true")
    arguments: argparse.Namespace = parser.parse_args()
    manifest: dict = json.loads(arguments.manifest.read_text(encoding="utf-8"))
    if manifest["format"] != 1:
        print("abi_python: manifest format " + str(manifest["format"]) + " is not 1", file=sys.stderr)
        return 1
    if arguments.target == "python":
        return write_or_check(render_python(manifest), PYTHON_OUTPUT, arguments.check)
    return write_or_check(render_cdef(manifest), CDEF_OUTPUT, arguments.check)


if __name__ == "__main__":
    sys.exit(main())
