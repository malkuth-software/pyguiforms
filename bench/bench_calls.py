#!/usr/bin/env python3
"""Per-call cost of the chatty paths under ctypes, cffi ABI mode and cffi API mode.

    GUI_FORMS_ABI_LIBRARY=... python3 bench/bench_calls.py [--cffi-abi] [--cffi-api]

Workloads, each N calls in a loop, best of ROUNDS rounds, reported in
nanoseconds per call:

- empty: runtime.clear_error, the cheapest slot (the binding's round trip);
- set_text: properties.set of a button's text, the view and value made once;
- raise_bare: Control::on_click's base for a button with no subscriber (the
  library's own raise);
- raise_callback: the same with one Python subscriber (raise_callback less
  raise_bare is the C-to-Python callback's cost).

The objects are made through pyguiforms.native (ctypes); the cffi variants
call the same library image with the same identities (one registry per
process, gf_abi.h).
"""

from __future__ import annotations

import ctypes
import os
import pathlib
import sys
import time

ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "bench"))

from pyguiforms import _abi, native  # noqa: E402

N: int = 200000
ROUNDS: int = 5


class Counter:
    """The Python subscriber: counts its calls."""

    def __init__(self) -> None:
        self.calls: int = 0

    def on_click(self, event: native.Event) -> None:
        self.calls += 1


def best_of(workload: object) -> float:
    best: float = float("inf")
    for unused_round in range(ROUNDS):
        started: int = time.perf_counter_ns()
        workload()
        elapsed: int = time.perf_counter_ns() - started
        per_call: float = elapsed / N
        if per_call < best:
            best = per_call
    return best


class CtypesWorkloads:
    def __init__(self, session: native.Session, button: native.ObjectReference,
                 bare: native.ObjectReference, raw: native.ObjectReference) -> None:
        self.clear_error = session.library.runtime.clear_error
        self.set = session.properties.set
        self.button: int = button.identity
        self.bare: int = bare.identity
        self.name: native.Utf8Text = native.Utf8Text("text")
        self.text: native.Utf8Text = native.Utf8Text("Click me")
        self.value: _abi.gf_value = _abi.gf_value()
        self.value.struct_size = ctypes.sizeof(self.value)
        self.value.kind = _abi.GF_VALUE_KIND_TEXT
        self.value.text = self.text.view
        self.value_reference = ctypes.byref(self.value)
        self.raiser: _abi.gf_base_raiser = _abi.gf_base_raiser()
        session.library.check(session.classes.base_raiser(_abi.GF_CLASS_CONTROL, native.control_hook_entry("on_click"),
                                                          ctypes.byref(self.raiser)))
        self.event: _abi.gf_event = _abi.gf_event()
        self.event.struct_size = ctypes.sizeof(self.event)
        self.event_reference = ctypes.byref(self.event)
        self.properties_record: ctypes.Structure = session.properties.record
        # A bare ctypes subscriber on a third button, without the hand-written
        # layer's registry lookup and Event wrapper, to compare with cffi's.
        self.raw: int = raw.identity
        self.raw_calls: int = 0
        self.raw_invoke = native.field_type(_abi.gf_callback, "invoke")(self.on_raw_click)
        self.raw_callback: _abi.gf_callback = _abi.gf_callback()
        self.raw_callback.struct_size = ctypes.sizeof(self.raw_callback)
        self.raw_callback.invoke = self.raw_invoke
        click: native.Utf8Text = native.Utf8Text("click")
        self.raw_subscription: _abi.gf_subscription = _abi.gf_subscription(0)
        session.library.check(session.events.subscribe(self.raw, click.view, ctypes.byref(self.raw_callback),
                                                       ctypes.byref(self.raw_subscription)))

    def on_raw_click(self, context: object, event: object) -> None:
        self.raw_calls += 1

    def raise_raw_callback(self) -> None:
        raiser = self.raiser
        raw: int = self.raw
        event = self.event_reference
        for unused_index in range(N):
            raiser(raw, event)

    def empty(self) -> None:
        clear_error = self.clear_error
        for unused_index in range(N):
            clear_error()

    def set_text(self) -> None:
        set_slot = self.set
        button: int = self.button
        name: _abi.gf_utf8_view = self.name.view
        value = self.value_reference
        for unused_index in range(N):
            set_slot(button, name, value)

    def set_text_unbound(self) -> None:
        # Reads the slot from the table record on every call, as naive
        # generated code would: ctypes builds a new function object each time.
        record: ctypes.Structure = self.properties_record
        button: int = self.button
        name: _abi.gf_utf8_view = self.name.view
        value = self.value_reference
        for unused_index in range(N):
            record.set(button, name, value)

    def raise_bare(self) -> None:
        raiser = self.raiser
        bare: int = self.bare
        event = self.event_reference
        for unused_index in range(N):
            raiser(bare, event)

    def raise_callback(self) -> None:
        raiser = self.raiser
        button: int = self.button
        event = self.event_reference
        for unused_index in range(N):
            raiser(button, event)


def report(binding: str, name: str, nanoseconds: float) -> None:
    print(binding.ljust(10), name.ljust(18), ("%.0f" % nanoseconds).rjust(7), "ns/call", flush=True)


def run_ctypes(workloads: CtypesWorkloads) -> None:
    report("ctypes", "empty", best_of(workloads.empty))
    report("ctypes", "set_text", best_of(workloads.set_text))
    report("ctypes", "set_text_unbound", best_of(workloads.set_text_unbound))
    report("ctypes", "raise_bare", best_of(workloads.raise_bare))
    report("ctypes", "raise_callback", best_of(workloads.raise_callback))
    report("ctypes", "raise_raw_callback", best_of(workloads.raise_raw_callback))


class CffiWorkloads:
    """The same workloads through cffi: ABI mode (libffi calls through the table slots) or API mode
    (the compiled module bench/_gf_cffi_api, whose C thunks call the slots directly)."""

    def __init__(self, mode: str, path: pathlib.Path, button: int, bare: int) -> None:
        self.mode: str = mode
        self.button: int = button
        self.bare: int = bare
        self.counter: Counter = Counter()
        if mode == "cffi-api":
            import _gf_cffi_api  # noqa: E402 (built by bench/cffi_api_build.py)
            self.ffi = _gf_cffi_api.ffi
            self.lib = _gf_cffi_api.lib
            self.ffi.def_extern(name="bench_invoke")(self.api_invoke)
            get_table = self.lib.bench_get_table
        else:
            import cffi  # noqa: E402
            self.ffi = cffi.FFI()
            self.ffi.cdef((ROOT / "bench" / "gf_abi_cdef.h").read_text(encoding="utf-8"))
            self.lib = self.ffi.dlopen(str(path))
            get_table = self.lib.gf_abi_get_table
        self.runtime = self.ffi.new("gf_runtime_table*")
        self.properties = self.ffi.new("gf_properties_table*")
        self.events = self.ffi.new("gf_events_table*")
        self.classes = self.ffi.new("gf_classes_table*")
        for table, table_id in ((self.runtime, _abi.GF_TABLE_RUNTIME), (self.properties, _abi.GF_TABLE_PROPERTIES),
                                (self.events, _abi.GF_TABLE_EVENTS), (self.classes, _abi.GF_TABLE_CLASSES)):
            status: int = get_table(table_id, _abi.ABI_MAJOR, _abi.ABI_MINOR, table, self.ffi.sizeof(table[0]))
            assert status == 0, status
        self.name_bytes = self.ffi.new("char[]", b"text")
        self.text_bytes = self.ffi.new("char[]", b"Click me")
        self.name = self.ffi.new("gf_utf8_view*", {"data": self.name_bytes, "size": 4})
        self.value = self.ffi.new("gf_value*")
        self.value.struct_size = self.ffi.sizeof("gf_value")
        self.value.kind = _abi.GF_VALUE_KIND_TEXT
        self.value.text.data = self.text_bytes
        self.value.text.size = 8
        self.raiser = self.ffi.new("gf_base_raiser*")
        status = self.classes.base_raiser(_abi.GF_CLASS_CONTROL, native.control_hook_entry("on_click"), self.raiser)
        assert status == 0, status
        self.event = self.ffi.new("gf_event*")
        self.event.struct_size = self.ffi.sizeof("gf_event")
        if mode == "cffi-api":
            self.callback = self.ffi.new("gf_callback*", {"struct_size": self.ffi.sizeof("gf_callback"),
                                                          "invoke": self.lib.bench_invoke})
        else:
            self.invoke_handle = self.ffi.callback("void(void*, gf_event*)", self.abi_invoke)
            self.callback = self.ffi.new("gf_callback*", {"struct_size": self.ffi.sizeof("gf_callback"),
                                                          "invoke": self.invoke_handle})
        self.click_text = self.ffi.new("char[]", b"click")
        self.click = self.ffi.new("gf_utf8_view*", {"data": self.click_text, "size": 5})
        self.subscription = self.ffi.new("gf_subscription*")
        status = self.events.subscribe(self.button, self.click[0], self.callback, self.subscription)
        assert status == 0, status

    def abi_invoke(self, context: object, event: object) -> None:
        self.counter.calls += 1

    def api_invoke(self, context: object, event: object) -> None:
        self.counter.calls += 1

    def empty(self) -> None:
        if self.mode == "cffi-api":
            thunk = self.lib.bench_clear_error
            runtime = self.runtime
            for unused_index in range(N):
                thunk(runtime)
            return
        clear_error = self.runtime.clear_error
        for unused_index in range(N):
            clear_error()

    def set_text(self) -> None:
        button: int = self.button
        name = self.name[0]
        value = self.value
        if self.mode == "cffi-api":
            thunk = self.lib.bench_set
            properties = self.properties
            for unused_index in range(N):
                thunk(properties, button, name, value)
            return
        set_slot = self.properties.set
        for unused_index in range(N):
            set_slot(button, name, value)

    def raise_with(self, target: int) -> None:
        event = self.event
        if self.mode == "cffi-api":
            thunk = self.lib.bench_raise
            raiser = self.raiser[0]
            for unused_index in range(N):
                thunk(raiser, target, event)
            return
        raiser = self.raiser[0]
        for unused_index in range(N):
            raiser(target, event)

    def raise_bare(self) -> None:
        self.raise_with(self.bare)

    def raise_callback(self) -> None:
        self.raise_with(self.button)


def run_cffi(workloads: CffiWorkloads) -> None:
    report(workloads.mode, "empty", best_of(workloads.empty))
    report(workloads.mode, "set_text", best_of(workloads.set_text))
    report(workloads.mode, "raise_bare", best_of(workloads.raise_bare))
    report(workloads.mode, "raise_callback", best_of(workloads.raise_callback))


def main() -> int:
    print("python", sys.version.split()[0], sys.implementation.name, "N", N, "best of", ROUNDS, flush=True)
    session: native.Session = native.open_session()
    print(session.version(), flush=True)
    root: native.ObjectReference = session.create("panel", "bench.root")
    button: native.ObjectReference = session.create_from_class("gf_button_class", _abi.GF_CLASS_BUTTON, "bench.button")
    bare: native.ObjectReference = session.create_from_class("gf_button_class", _abi.GF_CLASS_BUTTON, "bench.bare")
    session.insert_child(root, button, 0)
    session.insert_child(root, bare, 1)
    raw: native.ObjectReference = session.create_from_class("gf_button_class", _abi.GF_CLASS_BUTTON, "bench.raw")
    session.insert_child(root, raw, 2)
    counter: Counter = Counter()
    subscription: native.Subscription = session.subscribe(button, "click", counter.on_click)
    if "--cffi-abi" in sys.argv or "--cffi-api" in sys.argv:
        subscription.disconnect()
        mode: str = "cffi-api" if "--cffi-api" in sys.argv else "cffi-abi"
        cffi_workloads: CffiWorkloads = CffiWorkloads(mode, native.find_library(), button.identity, bare.identity)
        run_cffi(cffi_workloads)
        print("subscriber calls", cffi_workloads.counter.calls, flush=True)
    else:
        run_ctypes(CtypesWorkloads(session, button, bare, raw))
        print("subscriber calls", counter.calls, flush=True)
        subscription.disconnect()
    raw.release()
    bare.release()
    button.release()
    root.release()
    return 0


if __name__ == "__main__":
    sys.exit(main())
