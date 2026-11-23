# Form documents

A form document (`.form`) describes an interface in XML: its controls, their
stable IDs, their property values and their bindings. It holds no handlers
and no colours. Behaviour comes from your code, and looks from the theme.
GUI.Forms' own guide to the language is `docs/user/forms.md` in gui_forms;
pyguiforms reads the same documents at run time.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<form xmlns="urn:gui-forms:form:1" id="settings.window"
    text="Settings" client-size="360 150" accept-button="settings.ok">
  <panel id="settings.root">
    <check-box id="settings.autosave" text="Save automatically" bounds="16 16 240 28">
      <bind property="checked" to="autosave"/>
    </check-box>
    <label id="settings.status" text="Not saved yet." bounds="16 56 328 28" classes="status"/>
    <button id="settings.ok" text="OK" bounds="256 104 88 32"/>
  </panel>
</form>
```

```python
class Settings:
    def __init__(self):
        self.autosave = pyguiforms.Value(False)

settings = Settings()
form = pyguiforms.load_form("settings.form", model=settings)
form.settings_ok.on("click")(save)
form.run()
```

## What you get

`load_form` returns a `Form`:

- `form["settings.ok"]` is an object by its stable ID, and
  `form.settings_ok` is the same object (dots and hyphens become
  underscores);
- `form.window` is the window when the root is `form`;
- `form.root` is the root control;
- `form.accept_button` and `form.cancel_button`;
- `form.run()` runs the window;
- `release()` (or `with`) ends the bindings and gives back every object.

## Bindings

`<bind property="checked" to="autosave"/>` binds a property to the model's
attribute `autosave`, which must be a `pyguiforms.Value`.

- When the control is made, the property takes the value.
- Whenever the value changes, the property follows.
- The binding is two way unless it says `mode="one-way"`: the property's
  changes are written back into the value.

A `Value` is used on the UI thread. Set it with `value.value = x` or
`value.set(x)`, and `observe(function)` watches it.

## Refusals

A document is checked before anything is made, and every defect is
reported together as a `FormError`. Each diagnostic has the gui_forms code
(E801 to E821), the file, the line and the column:

```
settings.form:8:5: E804 form_property_unknown (colour): CheckBox
settings.form:11:5: E813 form_presentation_property (fore-color): set it in the theme ...
```

`read_form` does the checking alone, without the library, so a test or an
editor can check documents anywhere. `build_form(plan, model)` makes a
checked plan. When the library refuses a value there, the error is
reported as E807 at its place, and nothing made is kept.

## Differences from the C++ form compiler

The C++ build generates a class from a document; Python reads it at run
time. A few things are not loaded from Python yet. Each is refused with
E999, so a document never half-loads:

- Command bindings (`<bind property="command" .../>`);
- BindingSource fields (`field=`);
- a grid's `span` elements, and properties a parent type provides
  (`area`, `cell`).

`accept-button` and `cancel-button` are checked and kept on the `Form`,
but Enter and Escape do not act on them yet. The library cannot tell
pyguiforms which enumerations are flags, so a combination of choices is
checked by reading the value back after it is set.
