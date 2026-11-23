# Guide

pyguiforms puts GUI.Forms' retained model into Python. You make objects,
set their properties, subscribe to their events, put controls in a window
and run it. This page covers each of those in turn. The runnable versions
are in `examples/`.

## Objects

Every type in GUI.Forms' control schema is a class: `pyguiforms.Button`,
`pyguiforms.CheckBox`, `pyguiforms.DataGridView`, and so on. Controls
derive from `pyguiforms.Control`; components such as `Timer` and `Command`
derive from `pyguiforms.Component`.

```python
ok = pyguiforms.Button("settings.ok", text="OK", bounds=(280, 272, 88, 32))
```

- **The stable ID** is the first argument. It names the object for themes,
  automation and form documents, and is made of lowercase letters and
  digits, with single `-` between words and `.` between segments
  (`settings.ok-button`). Leave it out and pyguiforms issues one
  (`button12`, `text-box3`). An issued ID is never issued again.
- **Keyword arguments** set properties, in the order written.
- **Ownership:** an object holds one reference to its GUI.Forms object.
  `release()` gives it back once, and the finalizer does so as a last
  resort. `dispose()` ends the object: it leaves its parent and its
  subscriptions end. `with` does both:

  ```python
  with pyguiforms.Button(text="Temporary") as button:
      ...
  ```

- **Children:** a parent's Python object keeps its children, as the tree
  does. `add(*controls)` appends them, `remove(control)` takes one out, and
  `children` lists them.

## Properties

Properties are attributes under the schema's names:

```python
button.text = "Save"
button.enabled = False
button.text_alignment = "middle_center"
button.anchor = "top, right"           # a combination of flags
print(button.bounds)                   # Rect(x=..., y=..., width=..., height=...)
```

`get(name)`, `set(name, value)` and `reset(name)` do the same by name.
Writing a read-only property raises `AttributeError`, and so does a name
the type does not list.

| Kind | Python value |
|---|---|
| boolean | `bool` |
| signed and unsigned integer | `int` |
| number | `float` (an `int` is accepted) |
| text | `str` |
| point, size, rectangle, insets | `Point`, `Size`, `Rect`, `Insets`, or a plain tuple |
| color | `int` 0xRRGGBBAA (`pyguiforms.rgba(r, g, b, a)`) |
| font | `pyguiforms.Font(role, weight, italic, size, letter_spacing)` |
| image | `int`, an image id from `themes.load_image` |
| enumeration | the choice's name (`str`), or `"a, b"` for flags; its value as an `int` is accepted |
| collection | `list` of the items |

A value comes back as a copy. An enumeration that holds no named choice
comes back as its `int`.

## Events

`on(name)` is a decorator that subscribes a function to one of the type's
interactions (`Button.INTERACTIONS` lists them):

```python
@button.on("click")
def clicked(event):
    print(event.name, event.sender)
```

`on_change(name)` subscribes to a property's change. A handler receives
the event, which is lent only for the call. It offers:

- `event.fields()`, and `event.field(name)` for one field's value;
- `event.write(name, value)` for a writable field, such as a key event's
  `handled`;
- `event.cancel = True` where the event can be cancelled (a window's
  closing);
- `event.payload`.

`connect(name, handler)` returns the `Subscription`, and
`subscription.disconnect()` ends it. A subscription otherwise lasts until
its object is disposed or destroyed.

`raise_event("click")` raises an event the way the library would. A
person's click takes the same path from the raiser on, which makes it
useful in tests.

## Layout

Place controls with `bounds`, or with the layout properties (`dock`,
`anchor`, `margin`, `padding`) and the layout panels (`FlexPanel`,
`GridPanel`, `BlockPanel`). To change many controls with one layout pass
at the end:

```python
with panel.layout_suspended():
    panel.add(first, second, third)
```

## Windows

```python
window = pyguiforms.Window("Settings", 480, 320, minimum_width=320, minimum_height=200)
window.add(...)
window.run()
```

- A window shows a root control: a new panel, or the control passed as
  `root=`. `add` appends to it.
- `run()` shows the window and returns when it closes.
- `on("ready")`, `on("closing")` and `on("closed")` subscribe to the
  run's three moments. A closing handler may set `event.cancel = True`,
  and `event.field("reason")` says who closed the window: `"user"`,
  `"application"` or `"system"`.
- `close()` asks the window to close, as a program does.
- `post(function)` runs a function on the UI thread, from any thread.

## Threads

GUI.Forms has one UI thread: the thread that makes the first object. With
pyguiforms that is the Python main thread, which macOS requires anyway.

- Every object, property and event call runs on the UI thread. From
  another thread these calls raise `WrongThreadError` before they reach
  the library.
- To act from another thread, post to the UI thread with `window.post`.
- Handlers always run on the UI thread, one at a time.
- Releasing a reference works from any thread.

The registry of lent callbacks, the schema cache and the reference release
are locked, so the bindings need nothing more on a free-threaded CPython.

## Failures

- A refused call raises `GuiFormsError`, with the status, the table and
  slot, and the library's own message.
- A handler that raises never unwinds through C: the exception is caught
  where the library called Python.
  - In a call that returns to Python, it is raised there as
    `CallbackFailure`, whose `thrown` is the original exception.
  - Under `run()`, the window is asked to close and `run()` raises the
    `CallbackFailure`.
- To keep running instead, set a failure hook. One that returns `True`
  handles the failure and the loop carries on:

  ```python
  def report(failure):
      log.exception("handler failed", exc_info=failure.thrown)
      return True

  pyguiforms.set_failure_hook(report)
  ```
