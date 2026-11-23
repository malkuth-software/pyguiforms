#!/usr/bin/env python3
"""Builds bench/_gf_cffi_api, cffi's out-of-line API mode over the generated cdef.

The ABI exports one function and reaches everything else through table slots.
cffi's API mode compiles direct calls only for functions it declares, so this
module declares one C thunk per slot it calls (bench_set calls t->set), the
shape a generated API-mode or compiled binding would have for every slot.
Callbacks are extern "Python" (bench_invoke), cffi's compiled callbacks.
Run on a machine with a C compiler (the M4), never on the laptop.
"""

from __future__ import annotations

import pathlib

import cffi

HERE: pathlib.Path = pathlib.Path(__file__).resolve().parent
CDEF: str = (HERE / "gf_abi_cdef.h").read_text(encoding="utf-8")
EXPORT: str = ("gf_status gf_abi_get_table(gf_table_id table_id, uint32_t abi_major, uint32_t abi_minor, "
               "void* table, uint64_t table_capacity);")

THUNKS_DECLARED: str = """
gf_status bench_get_table(gf_table_id table_id, uint32_t abi_major, uint32_t abi_minor, void* table,
                          uint64_t table_capacity);
gf_status bench_clear_error(gf_runtime_table* table);
gf_status bench_set(gf_properties_table* table, gf_object object, gf_utf8_view name, const gf_value* value);
gf_status bench_raise(gf_base_raiser raiser, gf_object self, gf_event* event);
extern "Python" void bench_invoke(void* context, gf_event* event);
"""

# The library is opened at run time (dlopen in bench_get_table), so the module
# links against nothing of GUI.Forms; the declarations are the generated cdef.
THUNKS_DEFINED: str = """
#include <dlfcn.h>
#include <stdlib.h>
static gf_status bench_get_table(gf_table_id table_id, uint32_t abi_major, uint32_t abi_minor, void* table,
                                 uint64_t table_capacity) {
    static gf_status (*entry)(gf_table_id, uint32_t, uint32_t, void*, uint64_t) = 0;
    if (entry == 0) {
        void* handle = dlopen(getenv("GUI_FORMS_ABI_LIBRARY"), RTLD_NOW);
        if (handle == 0) return GF_STATUS_NOT_FOUND;
        entry = (gf_status (*)(gf_table_id, uint32_t, uint32_t, void*, uint64_t))dlsym(handle, "gf_abi_get_table");
        if (entry == 0) return GF_STATUS_NOT_FOUND;
    }
    return entry(table_id, abi_major, abi_minor, table, table_capacity);
}
static gf_status bench_clear_error(gf_runtime_table* table) { return table->clear_error(); }
static gf_status bench_set(gf_properties_table* table, gf_object object, gf_utf8_view name, const gf_value* value) {
    return table->set(object, name, value);
}
static gf_status bench_raise(gf_base_raiser raiser, gf_object self, gf_event* event) { return raiser(self, event); }
"""


def main() -> None:
    builder: cffi.FFI = cffi.FFI()
    declarations: str = CDEF.replace(EXPORT, "")
    builder.cdef(declarations + THUNKS_DECLARED)
    source: str = "#include <stdint.h>\n" + declarations + THUNKS_DEFINED
    builder.set_source("_gf_cffi_api", source)
    builder.compile(tmpdir=str(HERE), verbose=False)


if __name__ == "__main__":
    main()
