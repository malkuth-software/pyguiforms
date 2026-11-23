# pyguiforms

Python bindings over the GUI.Forms C ABI, generated from its audited ABI
manifest (gui_forms `manifests/abi/gf_abi.json`). This repository is at the
study stage: read `STUDY.md` first.

- `tools/abi_python.py`: the generator (the prototype of a Python target).
- `pyguiforms/_abi.py`: the generated 1:1 layer (ctypes). Do not edit.
- `pyguiforms/native.py`: the hand-written ownership, callback and failure layer.
- `examples/one_button.py`: the prototype, one window with one button.
- `bench/`: the binding-technology measurements.

MIT licence (`LICENSE`).
