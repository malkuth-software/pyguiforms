# Keeping the bindings in step with GUI.Forms

pyguiforms is generated from one pinned gui_forms commit, and every layer
checks that pin.

## The pin

`abi/` holds two files copied from that commit, plus a lock:

- `gf_abi.json`: the audited C ABI manifest (records, field offsets,
  function tables, constants and callbacks);
- `control-schema.json`: the control schema (types, properties,
  enumerations and interactions);
- `gui_forms.lock`: the commit and each copy's SHA-256.

To move the pin to a newer gui_forms:

```sh
python3 tools/pin_gui_forms.py ../gui_forms <commit>
python3 tools/abi_python.py           # writes _abi.py, _controls.py and the bench's cffi declarations
python3 -m unittest discover -s tests -t .
```

Review the generated diff the way you review an ABI change. New records
and slots appear in `_abi.py`, and new types and properties appear in
`_controls.py`.

## The checks

- **The lock:** `tools/abi_python.py --check` runs in CI. It fails when a
  pinned copy differs from its locked SHA-256, or when a generated file
  differs from what the pin gives. Generated files are never edited by
  hand.
- **Layout:** every record's size and field offsets as ctypes lays them
  out are compared with the manifest at import, on every host.
- **Negotiation:** each function table is asked for at the pinned ABI
  version. A slot the library does not serve answers "unsupported
  version" instead of calling through null.
- **The library a wheel carries:** `tools/build_wheel.py` refuses an
  archive whose ABI major differs from the pin or whose minor is older,
  and one whose library does not match its recorded SHA-256.

## Where the library comes from

gui_forms' release workflow packs the C ABI library from its deployment
build on each platform. The artifact is `gui-forms-abi-<platform>`, made
by `tools/package_abi_library.py`, and holds the library, the manifest it
was built from, its provenance and its licence notices.

pyguiforms' Wheels workflow takes the newest such run, or the run named
when dispatching, and then:

1. builds `py3-none-<platform>` wheels;
2. passes the Linux ones through auditwheel, which retags them
   manylinux;
3. installs each wheel on CPython 3.10 and 3.14 and runs the tests
   against the bundled library.

Nothing is published to PyPI.

## Rules for the hand-written layers

`native.py` adds only what the C ABI leaves to its caller: ownership,
callbacks, failures and the UI-thread rule. Everything about a type comes
from the schema, either the generated classes or the library's own schema
table at run time, never from a list kept by hand. The house style applies
throughout: named functions rather than lambdas or comprehensions, one
operation per expression, explicit ownership, and validated input.
