# pyguiforms

Python bindings for [GUI.Forms](https://github.com/malkuth-software/gui_forms),
a retained-mode desktop UI toolkit in C++ modelled on Windows Forms. The
bindings talk to GUI.Forms through its C ABI library (`gui_forms_abi1`) with
`ctypes`, so they are pure Python. One wheel per platform carries the library
and serves every CPython from 3.10. The bindings are written for
free-threaded builds too, though none has been tested yet.

```python
import pyguiforms

window = pyguiforms.Window("Hello", 320, 120)
button = pyguiforms.Button(text="Close", bounds=(24, 24, 120, 32))
window.add(button)

@button.on("click")
def clicked(event):
    window.close()

window.run()
```

## Why pyguiforms

GUI.Forms is retained mode: you build a tree of controls with properties
and events, as in Windows Forms, and the toolkit lays them out, paints them
and themes them. pyguiforms gives Python that model under the toolkit's
own names: `button.text`, `@button.on("click")`, form documents, theme
sheets.

How it compares with the usual choices (the full comparison, from each
project's own documentation, is in `STUDY.md` section 2):

- **Dear PyGui** is immediate mode on the GPU, and its callbacks run off
  the main thread by default. GUI.Forms is retained mode, needs no GPU, and
  calls back on the UI thread only.
- **PySide6 (Qt)** and **wxPython** are compiled C++ extensions generated
  from C++ headers. They ship large wheels: Qt's abi3 wheels are 62 to
  116 MB and do not cover free-threaded Python, and wxPython has a wheel
  per version and platform but none for Linux on PyPI. pyguiforms
  compiles nothing: one `py3-none` wheel per platform, about 14 MB with
  the library.
- **Tkinter** sends every call through an embedded Tcl interpreter as a
  command string, and some distributions leave it out. pyguiforms calls
  the C ABI directly. A property write takes about 0.4 µs.

## Install

```sh
pip install pyguiforms-<version>-py3-none-<platform>.whl
```

Wheels exist for macOS arm64 (macOS 14 or later), Windows x64, and Linux
x64 and arm64 (manylinux). CI builds them as workflow artifacts
(`.github/workflows/wheels.yml`); they are not on PyPI yet. Without a
wheel, install the source (`pip install .`) and point
`GUI_FORMS_ABI_LIBRARY` at a `gui_forms_abi1` library you built or
downloaded:

```sh
export GUI_FORMS_ABI_LIBRARY=/path/to/libgui_forms_abi.1.dylib
```

## A first window

`examples/first_window.py` is a text box, a button and a label:

```python
class Greeter:
    def __init__(self):
        self.window = pyguiforms.Window("First window", 360, 140)
        self.name = pyguiforms.TextBox(bounds=(12, 12, 220, 28))
        self.greet = pyguiforms.Button(text="Greet", bounds=(244, 12, 100, 28))
        self.greeting = pyguiforms.Label(text="Type a name.", bounds=(12, 56, 332, 28))
        self.window.add(self.name, self.greet, self.greeting)
        self.greet.on("click")(self.on_greet)

    def on_greet(self, event):
        self.greeting.text = "Hello, " + self.name.text + "."
```

Every schema type is a class (`pyguiforms.Button`, `pyguiforms.DataGridView`,
...). Its properties are attributes under the schema's names, and its
events are the type's `INTERACTIONS`. `docs/guide.md` covers objects,
properties, events, layout, windows, threads and failures.

The same window can come from a form document, bound to a model:

```python
form = pyguiforms.load_form("settings.form", model=settings)
form.settings_ok.on("click")(save)
form.run()
```

See `docs/forms.md`, `docs/themes.md` (theme sheets) and
`docs/automation.md`, which covers model tools and an MCP server over a
running window.

## How the bindings stay in step with the ABI

pyguiforms is generated from one pinned gui_forms commit.

- `abi/` holds that commit's ABI manifest and control schema, and
  `abi/gui_forms.lock` records the commit and each file's SHA-256.
- `tools/abi_python.py` generates `pyguiforms/_abi.py` (records, function
  tables, constants) and `pyguiforms/_controls.py` (one class per schema
  type). CI's `--check` fails when a generated file or a pinned copy
  drifts.
- At import, every record's layout is checked against the manifest.
- Each function table is negotiated at the pinned ABI version. A function
  the library does not serve answers "unsupported version" instead of
  crashing.
- A wheel bundles only a library whose ABI major matches the pin and
  whose minor is at least the pin's.

Moving to a new gui_forms is one command (`tools/pin_gui_forms.py`)
followed by the generator. `docs/maintaining.md` has the details.

## The repository

- `pyguiforms/`: the package. `_abi.py` and `_controls.py` are generated;
  `native.py`, `schema.py`, `values.py`, `controls.py`, `window.py`,
  `forms.py`, `binding.py`, `themes.py` and `automation.py` are written by
  hand.
- `tests/`: run them with `python -m unittest discover -s tests -t .`
  (pytest also collects them). The window tests need the library.
- `examples/`: `first_window.py`, `form_document.py` and `one_button.py`.
- `tools/`: the generator, the pin, the wheel builder.
- `bench/`: the binding-technology measurements behind `STUDY.md`.

MIT licence (`LICENSE`). The bundled library carries GUI.Forms' licence and
its third-party notices in `pyguiforms/_native/licenses/`.
