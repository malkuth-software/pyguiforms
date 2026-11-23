# pyguiforms: study

Python bindings over the GUI.Forms C ABI, generated from its audited ABI
manifest the way gui_forms `tools/abi_bindings.py` generates the C# layer.
This study maps the ABI to Python, chooses the binding technology from
measurements and from the alternatives' own documentation, describes
threads, packaging and the Pythonic API, records a working prototype, and
ends with the decisions the owner needs to make.

Status, 2026-11-22. The generator, the generated 1:1 layer, the hand-written
layer and the prototype in this repository run against an existing
`gui_forms_abi1` build (GUI.Forms 0.6.0, C ABI 1.6) on the M4. One window,
one button and one click callback work end to end on CPython 3.9, 3.14 and
3.15. Nothing is pushed. Nothing in gui_forms was changed.

Inputs:
- gui_forms `manifests/abi/gf_abi.json` at gui_forms `c1bbe4af3`. It is
  identical, byte for byte, to the manifest in the M4's integration
  workspace (`eebf24a8b`, checkpoint cp36), which built the library the
  prototype ran against.
- The library: the integration workspace's
  `.build/native-macos-arm64/gui-forms/libgui_forms_abi.1.6.0.dylib`
  (30,267,432 bytes, built 2026-11-22 15:36, sha256 `6ac5b3cb...4c12`),
  copied to `/tmp/pyguiforms_study/lib/` on the M4 so that a rebuild could
  not change it during the runs.

Repository layout:

| Path | What it is |
|---|---|
| `tools/abi_python.py` | The generator: `python` writes `pyguiforms/_abi.py`, `cdef` writes `bench/gf_abi_cdef.h` (C declarations for cffi). `--check` fails when an output differs from what the manifest gives. |
| `pyguiforms/_abi.py` | The generated 1:1 layer (ctypes), 3,440 lines. Do not edit. |
| `pyguiforms/native.py` | The hand-written layer: loading, negotiation, failures, callbacks, ownership. |
| `examples/one_button.py` | The prototype. |
| `bench/bench_calls.py`, `bench/cffi_api_build.py` | The binding-technology measurements. |

## 1. The ABI's surface mapped to Python

The manifest (format 1, ABI 1.6, four targets: x86_64 Windows GNU and MSVC,
x86_64 Linux, aarch64 macOS) lists:

| Manifest entry | Count | Python form | Generated or hand-written |
|---|---|---|---|
| Export (`gf_abi_get_table`) | 1 | `bind_gf_abi_get_table(library)` sets `restype` and `argtypes` | Generated |
| Function tables (`kind: table`) | 27 | `ctypes.Structure` whose slots are `CFUNCTYPE` fields; `TABLE_IDS` maps each to its `GF_TABLE_*` | Generated layout. Negotiation, the missing-slot rule and slot binding are hand-written (`native.Table`). |
| Records (`record`) | 23 | `ctypes.Structure` | Generated |
| Extensible records (`extensible`) | 80 | `ctypes.Structure`; the caller sets `struct_size` | Generated layout. Filling `struct_size` and keeping lent storage alive are hand-written. |
| Class-table segments (`segment`) | 11 | `ctypes.Structure` of `gf_hook_entry` fields | Generated |
| Class tables (`class`) | 34 | `ctypes.Structure` of header plus segment pointers | Generated layout. Their lifetime (borrowed by every object made from them) is hand-written. |
| Scalar typedefs | 109 | the ctypes fixed-width type (`gf_object = ctypes.c_uint64`) | Generated |
| Constants | 699 | module `int`s (`GF_STATUS_OK = 0`) | Generated |
| Callback typedefs | 2 | `CFUNCTYPE` (`gf_base_raiser`, `gf_hook_entry`) | Generated |

What maps mechanically. Every type in the dialect has an exact ctypes
equivalent. The dialect admits fixed-width integers, `double`, pointers,
typedef'd function pointers and fixed arrays (`uint8_t[48]`, `double[20]`),
and nothing else: no enums, bitfields, unions, `bool` or `size_t`. Records
have no implicit padding. So ctypes lays out all 175 records exactly as the
manifest does. The generated `check_layout()` compares every size and every
field offset with the manifest's numbers (C#'s `Layout.check`). On the M4
under CPython 3.14 it found no mismatch in 0.1 ms; importing `_abi` takes
25 ms. Records larger than 16 bytes are passed by pointer, and the two
16-byte by-value records (`gf_utf8_view`, `gf_logical_point`) pass through
ctypes correctly. Callbacks take pointers only, so ctypes' limits on
structures in callbacks never apply.

What needs the hand-written layer. Every item below is an invariant the
C ABI leaves to its caller, and each is a few lines in `native.py`:

- **Negotiation and missing slots.** Each table is negotiated once at the
  manifest's version. A slot past the negotiated `struct_size`, or a null
  one, answers `GF_STATUS_UNSUPPORTED_VERSION` instead of calling through
  null. This is the rule of gui_forms `gf_abi.hpp`.
- **Slot binding.** ctypes has no original-object return: reading a
  `CFUNCTYPE` field builds a new function object on every access. The
  hand-written `Table` reads each slot once. Measured cost of not doing so:
  +24 to +69 ns per `properties.set` (section 2).
- **Status codes.** A status other than OK becomes `GuiFormsError`, carrying
  the calling thread's `runtime.error_detail` (table, slot, message). Only
  the caller knows which statuses it expects (`NOT_FOUND`,
  `BUFFER_TOO_SMALL`), so `check` is called where a failure is exceptional,
  as C#'s `Abi.check` is.
- **Text.** `gf_utf8_view` is never terminated, so `char*` is generated as
  `POINTER(c_char)`, not `c_char_p`. `Utf8Text` owns the encoded bytes and
  the view of them. `read_view` copies lent text out with
  `ctypes.string_at(data, size)`.
- **Callbacks.** A `gf_callback`'s context is a key into `CallbackRegistry`.
  A key is issued once, never reused, and checked for exhaustion. The
  library's `release` forgets it, and a refused registration is forgotten by
  the caller, because the library then never calls release. One invoke
  trampoline and one release trampoline are made at import, for the whole
  process, so lending a callback allocates no executable closure.
- **Event lending.** `Event` wraps the `gf_event*` for one invoke and
  refuses reads after it.
- **Ownership.** `ObjectReference` gives its `gf_object` reference back
  exactly once: through `release`, the context manager, or the finalizer as
  a last resort, which is safe because `objects.release` is callable from
  any thread. `Subscription` disconnects once, and treats `STALE_HANDLE` (a
  source that has already ended) as done.
- **Class tables.** The table is borrowed by every object made from it, so
  the session keeps one table per class for its whole life.
- **Values.** `gf_value` is a tagged record (`kind` selects the field).
  Converting between Python values and `gf_value` belongs in the Pythonic
  layer, driven by the schema's property kinds (`schema.property_at`). The
  prototype converts text and rectangles only.

## 2. Binding technology

### Measurements

The measurements were taken on the M4 (Apple M4), against the library
above, 200,000 calls per round, best of 5 rounds, in nanoseconds per call
(`bench/bench_calls.py`):

| Workload | ctypes 3.9 | ctypes 3.14 | ctypes 3.15 | cffi ABI 3.9 | cffi API 3.9 |
|---|---|---|---|---|---|
| `empty`: `runtime.clear_error`, the binding's round trip | 60 | 67 | 71 | 47 | 50 |
| `set_text`: `properties.set` of a button's text | 393 | 473 | 464 | 250 | 227 |
| `set_text`, slot read from the record on each call | 417 | 542 | 520 | - | - |
| `raise_bare`: a click raised with no subscriber | 343 | 372 | 382 | 225 | 213 |
| `raise_raw_callback`: the same, one bare Python subscriber | 538 | 560 | - | 405 | 391 |
| `raise_callback`: the same through `native`'s registry and `Event` | 888 | 743 | 752 | - | - |

How to read the table:
- **The library's own work.** It is about 180 ns for `set_text` and about
  160 ns for a raise: the cffi API rows less `empty`.
- **What ctypes adds.** It costs about 140 to 250 ns more than cffi per
  property set. That is argument conversion: the by-value view, `byref`, and
  the `argtypes` checks. CPython 3.14 and 3.15 are slower here than 3.9.
- **The callback.** A C-to-Python callback costs about the same in all
  three: 195 ns (ctypes), 180 ns (cffi ABI), 178 ns (cffi API, `extern
  "Python"`). Most of it is the Python call itself.
- **API mode.** Out-of-line API mode gains little over ABI mode: 23 ns on
  `set_text`. The ABI reaches everything through table slots, and cffi
  compiles only the functions it declares, so API mode needs a generated C
  thunk per slot (`bench_set` calls `table->set`). That is a compiled
  extension in all but name.
- **The registry and `Event` wrapper.** These cost 180 to 350 ns per event.
  This is the first thing to make cheaper, for example with a `__slots__`
  `Event` and no lock on the invoke path, since invokes run only on the UI
  thread.
- **Scale.** At 470 ns, one frame of 16.7 ms has room for about 35,000
  property sets. The chatty paths are not a reason to compile.

Not measured: PyPy (not installed on the M4) and free-threaded CPython
(no 3.13t or 3.14t build on the M4: both Homebrew Pythons report
`Py_GIL_DISABLED = 0`). Section 3 gives what the documentation says about
both.

### What the alternatives do, from their own documentation

- **Dear PyGui** wraps Dear ImGui. Its README calls Dear PyGui
  "fundamentally different than other Python GUI frameworks", states that it
  "uses the immediate mode paradigm and your computer's GPU", that it is
  "written in C/C++", and lists the backends: DirectX 11, Metal, OpenGL 3
  and OpenGL ES. Callbacks are "not run on the main thread" by default.
  `manual_callback_management` hands the queue to the program, which drains
  it with `run_callbacks` (docs, item callbacks). PyPI 2.3.1 has 26
  version-specific wheels (cp38 to cp314, four platforms, about 2 to
  2.7 MB), no abi3 wheel, no free-threaded wheel and no sdist.
  *Where it hurts for us:* a compiled CPython extension needs one wheel per
  CPython version per platform, plus a separate free-threaded build. It is
  immediate mode, which gui_forms `AGENTS.md` excludes ("do not introduce an
  immediate-mode control API"). It needs a GPU, and GUI.Forms has no GPU
  capability. It also moves callbacks off the program's main thread, which
  the GUI.Forms threads rule forbids: a UI thread, and callbacks only there.
- **PySide6 (Qt).** It is generated with Shiboken: a generator that turns
  C++ headers and a typesystem description into CPython C++ extension code.
  The Shiboken generator is a separate package that does not get installed
  with PySide, because it is not required. PySide6 ships abi3 wheels (the
  limited API, one wheel for many CPython versions). PySide6-Essentials
  6.12.0 has five wheels tagged `cp310-abi3`, from 62.1 MB (Windows arm64)
  to 116.0 MB (macOS universal2), and requires Python 3.10 to 3.15. The Qt
  FAQ's install sample shows the full PySide6 wheel at 170.5 MB.
  *Where it hurts:* the binding is C++ generated against C++ headers, so it
  carries a C++ ABI and a compiler on every platform. abi3 saves the
  per-version matrix, but the free-threaded build does not support the
  limited API (CPython free-threading HOWTO), so abi3 does not cover 3.13t
  and later.
- **wxPython (Phoenix)** is "a set of Python extension modules that wrap the
  GUI components of the popular wxWidgets" library, which uses native
  widgets (wxPython overview). The Phoenix README describes the pipeline:
  `dox`, `etg` (Extractor-Tweaker-Generator scripts), `sip` (which "produces
  the C++ code"), then `build`. It warns that the build is complicated and
  points most users to prebuilt binaries. wxPython 4.3.2 on PyPI has 30
  files: a 65.9 MB sdist and version-specific Windows and macOS wheels of
  17 to 20 MB. PyPI has no Linux wheel; the Phoenix README lists Linux
  wheels per Ubuntu release, which depend on system libraries.
  *Where it hurts:* a version-by-platform wheel matrix, no portable Linux
  wheel, and a build only experts manage.
- **Tkinter.** The Python docs describe the call path: tkinter "assembles a
  Tcl/Tk command string", passes it to the internal `_tkinter` binary
  module, which "calls the Tcl interpreter to evaluate it". Each `Tk` object
  embeds a Tcl interpreter and records the thread that created it. Calls
  from other threads are posted to that interpreter's queue, and they fail
  when its event loop is not running. The official installers bundle Tcl/Tk
  9.0, and the module is optional for distributors.
  *Where it hurts:* every operation is a string evaluated by a second
  language runtime. Distributions may leave the module out.
- **ctypes** (standard library): `CDLL` releases the GIL around every call.
  A `CFUNCTYPE` object must be kept alive "as long as they are used from C
  code" or the program crashes. A callback from a thread created outside
  Python gets "a new dummy Python thread on every invocation". On
  free-threaded builds, concurrent access to one ctypes object is safe, but
  access across several objects needs a lock. Unions and bit-field records
  cannot be passed by value, and the ABI has neither.
- **cffi.** ABI mode needs no compiler. Out-of-line API mode needs "a C
  compiler to run example_build.py, once", and "at runtime, the API mode is
  faster than the ABI mode" (cffi overview). Old-style `ffi.callback()`
  needs writable and executable memory. On macOS that requires the
  `com.apple.security.cs.allow-unsigned-executable-memory` entitlement. On
  Linux, systemd's `MemoryDenyWriteExecute` can block it, and the docs
  recommend `extern "Python"` instead (cffi, using). cffi aims to "support
  both PyPy and CPython" (cffi goals). PyPy's own docs call cffi "the
  recommended way" and say "ctypes' performance is not as good as CFFI's"
  (PyPy, extending). cffi 2.1.1 ships cp314t and cp315t free-threaded
  wheels and requires Python 3.10 or later.

### Recommendation

**ctypes for the generated 1:1 layer, now.** The reasons:

1. **One wheel per platform.** The package is pure Python plus the
   gui_forms library, and that library does not link against CPython. So
   one `py3-none-<platform>` wheel serves every CPython version,
   free-threaded builds and PyPy. Compiled bindings need the per-version
   matrices that Dear PyGui (26 wheels) and wxPython (30 files) ship.
2. **No compiler** anywhere: not on users' machines, and not in pyguiforms'
   CI beyond the gui_forms build that already exists.
3. **No dependency.** ctypes is in the standard library.
4. **The measured cost is small next to a frame.** Generated cffi ABI mode
   is about 40% faster per property set, and API mode barely faster than
   that.
5. **A cheap later switch.** The generator already writes the cffi
   declarations (`cdef`), and cffi read them unchanged for both benchmarks.
   Moving to cffi ABI mode later changes only the hand-written layer's call
   sites, not the generator's input.

Revisit this if PyPy becomes a target, where ctypes is slow and cffi is
PyPy's recommended path, or if profiling a real program shows binding
overhead dominating. Decision 1 states the options.

## 3. Threads, the GIL and callbacks

The rules come from gf_abi.h (Threads, Callbacks):
- The first thread that creates an object becomes the library's UI thread.
  Every table function runs on it alone, except `objects.retain`,
  `objects.release` and `dispatch.begin_invoke`.
- The library calls callbacks only on the UI thread, never two at once, and
  calls each callback's release exactly once.
- A callback may call any function, including the ones that end it.

How this maps to Python:

- **The UI thread is the Python main thread.** On macOS the host must run
  AppKit on the process's main thread, and Python's main thread is that
  thread. The pythonic layer should therefore refuse to create the first
  object off the main thread, with a clear error, rather than let the
  library answer `GF_STATUS_WRONG_THREAD` later.
- **The GIL.** ctypes releases it around every library call, `windows.run`
  included. So other Python threads run while the event loop waits, and
  every callback takes the GIL for its invoke. The prototype's watchdog
  thread shows this: it calls `dispatch.begin_invoke` from off the UI
  thread during the loop, and the callback runs on the main thread
  ("watchdog: closing the window" in section 6). Because the library calls
  back only on the UI thread, which is a Python-created thread, ctypes'
  dummy-thread case for foreign threads does not arise.
- **No exception crosses into C.** The invoke trampoline catches every
  `BaseException`, `KeyboardInterrupt` included, and records it for the
  thread as a `CallbackFailure`. Where it surfaces depends on the
  innermost library call, the same split C#'s `CallbackFailure` makes:
  - **A call that returns into Python** (`properties.set` raising an event
    synchronously, `run_pending`, a click raised directly): the caller's
    `check` rethrows the failure on return.
  - **The event loop** (`windows.run`): no Python caller gets control until
    the loop ends. The prototype's policy is to ask the running window to
    close (`request_close`, which a callback may call), let `run` return,
    and raise the failure from `run`. The prototype's `--fail` run shows
    it: `run raised CallbackFailure: ... ValueError: the click handler
    failed on purpose`. C# instead raises the failure through an
    `unhandled` event and defaults to fail-fast. Decision 3.
  - **Nested failures.** A failure rethrown inside an outer callback (a
    posted callback that raised a click whose handler failed) is recorded
    once, not wrapped twice.
- **Re-entrancy.** Callbacks may call back into the library, and the
  library defines the order: a subscription made during an emission is
  first called by the next emission, and one ended during an emission is
  not called again (GF_TABLE_EVENTS). The registry therefore takes its lock
  only around its own dictionary and calls no handler under it.
- **Ctrl-C.** CPython runs signal handlers only while Python code runs. A
  `KeyboardInterrupt` during `windows.run` is therefore seen at the next
  callback, where it becomes a failure and closes the window under the
  policy above. A window with no callbacks would not see it until it
  closes. The Pythonic layer should install a SIGINT handler that posts
  `request_close` through `begin_invoke`. Not prototyped.
- **Free-threaded CPython (3.13t+).** ctypes works there. The only shared
  mutable state in `native.py` is the registry, which takes a lock; per-thread
  failures live in `threading.local`. Because the library serializes all
  callbacks onto the UI thread, a free-threaded build changes nothing in
  the callback contract. What it does change is that Python threads really
  run in parallel with the UI thread, so a program's own shared state needs
  its own locks. ctypes' docs say concurrent access to one ctypes object is
  safe, but access across several objects is not. Not measured: no
  free-threaded build on the M4 (section 2).

## 4. Packaging

- **The wheels.** One wheel per platform, tagged `py3-none-<platform>`,
  holding the package and the gui_forms library in `pyguiforms/_native/`:
  - `macosx_14_0_arm64`: the M4 builds against the macOS 14 runtime;
  - `win_amd64`: `gui_forms_abi1.dll`;
  - `manylinux_2_<n>_x86_64` and `manylinux_2_<n>_aarch64`:
    `libgui_forms_abi.so.1`.

  The file names are cmake/CAbi.cmake's, as the C# `NativeLibraryName`
  records them. The library is self-contained (owner decision 2026-11-15):
  on macOS it imports only system frameworks (checked with `otool -L`).
  The macOS library is 30.3 MB, 14.2 MB gzipped, so a wheel is about 14 MB.
  That is between Dear PyGui's 2 MB and PySide6's 62 to 116 MB.
- **Finding the library at run time.** `native.find_library` uses
  `GUI_FORMS_ABI_LIBRARY` when it is set (development, and the
  prototype), otherwise the bundled copy. It loads by absolute path, so no
  `DYLD_*`, `LD_LIBRARY_PATH` or `PATH` search is involved. A missing
  library fails at `open_session` with the path it tried.
- **Linux.** The library must satisfy the manylinux policy (`auditwheel
  show`). Its X11, xcb and Wayland imports need checking against the
  policy's allowed libraries before the Linux tags are promised. To verify.
- **CI** (a GitHub Actions matrix in pyguiforms, once the repository
  exists):
  1. Pin gui_forms by commit (`gui_forms.lock`, as gui_forms_tests pins
     it).
  2. Fetch the manifest and the per-platform `gui_forms_abi1` artifacts
     that gui_forms CI already builds. Never rebuild GUI.Forms here.
  3. Run `tools/abi_python.py python --check` and `cdef --check`.
  4. On each platform: import, call `check_layout()`, and run the prototype
     with `--auto`. Linux needs a display (Xvfb), or the headless host if
     the ABI library can select it.
  5. Build the four wheels and test-install each in CPython 3.10, the
     newest CPython and its free-threaded build.

  Publishing to PyPI is a later, separate decision.

## 5. The Pythonic API's shape

The same window, written both ways. Neither layer exists yet beyond the
prototype's `Session`.

**Close to C#'s Forms API** (`GuiForms.Forms`: a `Button(stable_id)` made
through its class table, Windows Forms names, `On*` hooks):

```python
from pyguiforms.forms import Application, Button, Panel


class MainForm(Panel):
    def __init__(self) -> None:
        super().__init__("main.root")
        self.ok_button = Button("main.ok-button")
        self.ok_button.Text = "Click me"
        self.ok_button.Bounds = (24, 24, 160, 36)
        self.ok_button.Click += self.ok_button_Click
        self.Controls.Add(self.ok_button)

    def ok_button_Click(self, sender: Button, e: EventArgs) -> None:
        print("clicked")
        self.Close()


Application.Run(MainForm(), title="pyguiforms", width=320, height=120)
```

**Idiomatic Python first** (properties, events as decorators, context
managers), keeping the schema's own snake_case names, which are already
Pythonic (`text`, `bounds`, `click`):

```python
import pyguiforms as gf


with gf.Window("pyguiforms", width=320, height=120) as window:
    ok_button = gf.Button("main.ok-button", text="Click me", bounds=(24, 24, 160, 36))
    window.add(ok_button)

    @ok_button.on("click")
    def on_ok_click(event: gf.Event) -> None:
        print("clicked")
        window.close()

    window.run()
```

Two things shape the choice:
- **The names.** The schema already spells properties and interactions in
  snake_case, so the idiomatic API needs no renaming table. The C#-shaped
  API has to map every name to Windows Forms casing.
- **Subclass hooks.** The class tables (`gf_abi_classes.h`) map naturally
  onto Python subclassing in both shapes. A subclass that defines
  `on_click(self, event, base)` gets a class table whose `on_click` entry
  is the trampoline. `base` runs the stock raiser, which calls the
  subscribers.

House style shapes the idiomatic API too. Handlers are named functions (no
lambdas). The decorator only registers a named function. `with` ties the
window's objects to a scope.

Recommendation: idiomatic Python first, with the schema's names and
`On*`-style hooks available through subclassing, so that a Windows Forms
programmer still finds every member under its schema name. Decision 4.

## 6. The prototype

The prototype is `examples/one_button.py`. It uses the generated layer plus
`native.py`, and nothing else:
1. Load the library and negotiate the runtime, objects, properties, events,
   dispatch, windows and classes tables.
2. Create a `panel` root with `objects.create`, and a `button` with
   `classes.create`. The button needs an override-free class table so that
   its click raiser has a base the automatic click can run. A stock button
   from `objects.create` is refused by `classes.base_raiser` with
   `GF_STATUS_WRONG_HANDLE_KIND`: "the object was not made from a class
   table". The first run hit this refusal, and it came back as a
   `GuiFormsError` raised from `run`, as designed.
3. Set the button's `text` and `bounds` with `properties.set`, and insert it
   under the root.
4. Subscribe to its `click` with a Python method.
5. `windows.run` the root, with `ready`, `closing` and `closed` callbacks.
6. With `--auto`, `ready` posts a callback (`dispatch.begin_invoke`) that
   raises the click through `Control::on_click`'s base
   (`classes.base_raiser`), the path a person's click takes from the raiser
   on. The click handler asks the window to close.
7. A watchdog thread posts a close after 20 seconds from off the UI thread.

What ran, on the M4 over ssh (the console session's window server shows the
window), with
`GUI_FORMS_ABI_LIBRARY=/tmp/pyguiforms_study/lib/libgui_forms_abi.1.dylib`:

```text
$ python3.14 examples/one_button.py --auto
GUI.Forms 0.6.0, C ABI 1.6 from libgui_forms_abi.1.dylib
ready: event 'ready' sender 0x100000001
posted: event 'invoke' on thread MainThread
click: event 'click' sender 0x100000002 count 1
closing: reason user
closed: reason user
run returned; clicks 1
pending callbacks run: 0 | handlers still lent: 0
exit 0
$ python3.14 examples/one_button.py --auto --fail
GUI.Forms 0.6.0, C ABI 1.6 from libgui_forms_abi.1.dylib
ready: event 'ready' sender 0x100000001
posted: event 'invoke' on thread MainThread
click: event 'click' sender 0x100000002 count 1
closing: reason user
closed: reason user
run raised CallbackFailure: a GUI.Forms callback raised ValueError: the click handler failed on purpose | cause: ValueError('the click handler failed on purpose')
pending callbacks run: 0 | handlers still lent: 0
exit 3
$ python3.14 examples/one_button.py   (nobody clicks: the watchdog closes it)
GUI.Forms 0.6.0, C ABI 1.6 from libgui_forms_abi.1.dylib
ready: event 'ready' sender 0x100000001
watchdog: closing the window
closing: reason user
closed: reason user
run returned; clicks 0
pending callbacks run: 0 | handlers still lent: 0
exit 0
/usr/bin/python3 (3.9.6) --auto: exit 0, 1 click
/opt/homebrew/bin/python3.15 --auto: exit 0, 1 click
40 alternating --auto / --auto --fail runs: 0 unexpected results
```

What the output shows:
- **Every lent callback was released.** "handlers still lent: 0": the
  click subscription, the three run callbacks and the posted callbacks each
  had their release called exactly once.
- **The handler's exception crossed back as a Python exception**, not as an
  unwind through C.
- **Cross-thread posting works during the loop** (the watchdog run).

Two findings from the runs:
- **The close reason.** Every close here was the program's
  (`windows.request_close`), yet `closing` and `closed` report reason
  `user`. gf_abi.h defines `application` (1) as "the program closed it".
  This is reported to the coordinator as a possible library defect on the
  macOS host. Not checked on other hosts.
- **A false alarm.** An earlier repeat loop appeared to lose the posted
  click in every other run. The cause was the loop: zsh does not split an
  unquoted `$a`, so `--auto --fail` reached the program as one argument and
  neither flag was set. Traced and corrected, the 40-run repeat has no
  unexpected result.

## 7. Decisions for the owner

**Decision 1: binding technology for the generated layer.**
1. **ctypes** (standard library). No dependency and no compiler. One wheel
   per platform for every CPython version, free-threaded builds and PyPy.
   Measured at 393 to 473 ns per property set and about 195 ns per
   callback. Slow on PyPy.
2. **cffi ABI mode.** About 40% faster per property set (250 ns), and the
   callback cost is the same. Adds the cffi dependency, which ships
   free-threaded wheels for 3.14t and 3.15t and requires Python 3.10 or
   later. PyPy's recommended path. Still one wheel per platform.
3. **cffi API mode, or a compiled extension.** Only 23 ns faster than
   option 2 per property set, because table slots need a generated C thunk
   each. A compiler in CI and a wheel per CPython version per platform,
   plus separate free-threaded wheels (the limited API does not cover
   them).

Recommendation: **1, ctypes**. Keep the generator's cffi output, so that
moving to option 2 later changes only call sites.

**Decision 2: where the Python generator lives.**
1. **A third target in gui_forms `tools/abi_bindings.py`.** One tool for
   all bindings, and gui_forms CI can `--check` it. But its output lives in
   another repository, so the check would need that checkout.
2. **A sibling tool in gui_forms** (`tools/abi_python.py`). The same
   trade-off, as a separate file.
3. **In pyguiforms, reading a pinned manifest** (`gui_forms.lock`, as
   gui_forms_tests pins gui_forms). Its `--check` runs in pyguiforms CI. A
   manifest change reaches Python when the pin moves.

Recommendation: **3**. The output and the code that depends on it live in
pyguiforms, the manifest is the only interface, and gui_forms needs no
knowledge of Python. Move to option 1 only if gui_forms CI must refuse ABI
changes that break Python.

**Decision 3: what a callback's exception does during the event loop.**
1. **Close the window and raise from `run`** (the prototype). The failure
   surfaces where Python expects it, as an exception from the call that
   was running.
2. **Fail fast** (C#'s default). The process ends at once with the failure.
3. **Report and carry on.** The failure goes to an `unhandled` hook,
   default printing it, and the loop continues, as Windows Forms'
   `ThreadException` does.

Recommendation: **1 by default, with an `unhandled` hook** a program can
set to choose 3. No failure is silent, and none kills the process before
Python's own handling sees it.

**Decision 4: the Pythonic API's shape.**
1. **Close to C#'s Forms API.** Windows Forms casing, `+=` events,
   `Controls.Add`. Familiar to Windows Forms programmers, foreign to Python
   ones, and a renaming table to keep.
2. **Idiomatic Python first.** The schema's snake_case names, decorator
   events, context managers, and subclass hooks from the class tables.

Recommendation: **2**.

**Decision 5: supported Pythons.**
1. **CPython 3.10 and later**, including free-threaded 3.14t and later,
   each tested in CI. This matches the floor of cffi 2.x and PySide6.
2. **CPython 3.9 and later.** The prototype runs on 3.9, but 3.9 is past
   its end of life.
3. **Option 1 plus PyPy.** This argues for cffi (decision 1, option 2).

Recommendation: **1**.

**Decision 6: where the wheels' native library comes from.**
1. **gui_forms CI's per-platform artifacts at the pinned commit.**
   pyguiforms never compiles GUI.Forms.
2. **pyguiforms CI builds gui_forms itself.**

Recommendation: **1**. One build of the library, the one gui_forms tests.

**Decision 7: the LICENSE copyright line.** gui_forms' LICENSE names the
owner. The study's rules forbid personal details in files, so pyguiforms'
LICENSE reads "Copyright (c) 2026 The pyguiforms authors".
1. Keep "The pyguiforms authors".
2. The owner puts in their own name, as in gui_forms.

Recommendation: **the owner's call**. Option 1 stands until they say
otherwise.
