# pyguiforms

Python bindings for GUI.Forms over its C ABI (`gui_forms_abi1`), generated
from the ABI manifest and control schema of one pinned gui_forms commit.
The design is in `STUDY.md`; the full README (alternatives, install, a
first window, how the bindings keep up with the ABI) comes with the wheels.

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

- `abi/`: the pinned gui_forms inputs and `gui_forms.lock` (the commit and
  each copy's SHA-256), written by `tools/pin_gui_forms.py`.
- `tools/abi_python.py`: the generator; `--check` fails when a generated
  file differs from the pinned inputs.
- `pyguiforms/_abi.py` and `pyguiforms/_controls.py`: generated. Do not edit.
- `pyguiforms/native.py`, `schema.py`, `values.py`, `controls.py`,
  `window.py`: the hand-written layers.
- `tests/`: `python -m unittest discover -s tests -t .` (pytest also
  collects them); the window tests need `GUI_FORMS_ABI_LIBRARY`.
- `examples/`: `first_window.py` and the study's `one_button.py`.
- `bench/`: the binding-technology measurements.

MIT licence (`LICENSE`).
