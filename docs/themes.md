# Themes

A GUI.Forms window takes its look from the theme: CSS theme sheets whose
rules select controls by type, stable ID and class. A form document names
roles with `classes`, and the sheet gives each role its look. The language
is gui_forms' `docs/user/theme-language.md`.

```python
import pathlib
from pyguiforms import themes

warnings = themes.load_sheet(pathlib.Path("app.theme.css").read_text(encoding="utf-8"), "app")
```

- **One theme per process:** the library holds one theme for every window.
  A sheet loaded before `run` applies from the first frame. One loaded
  during a run replaces the running window's theme at once.
- **Refusal:** a refused sheet changes nothing and raises `ThemeError`.
  Its `findings` give each problem's severity, code, file, line, column,
  rule, property and detail. A sheet that loads with warnings returns
  them.
- `themes.reset()` makes the built-in theme current again.
- `themes.theme_id()` names the theme in use.
- **Published values:** `publish_value(name, number)` gives sheets a value
  they read as `var(--name)`. Every open window repaints the parts that
  read it. `withdraw_value` and `published_value` complete the set.
- **Images:** `load_image(png_bytes)` returns the id an image property
  takes, and `remove_image(id)` removes one.

All of these run on the UI thread.
