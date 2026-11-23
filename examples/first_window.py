"""A first window: a text box, a button that greets, and a label.

    GUI_FORMS_ABI_LIBRARY=/path/to/libgui_forms_abi.1.dylib python3 examples/first_window.py [--auto]

With --auto the window types a name, clicks the button itself and closes,
so the example can run unattended.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import pyguiforms  # noqa: E402


class Greeter:
    """The window, its controls and its handlers."""

    def __init__(self, automatic: bool) -> None:
        self.automatic: bool = automatic
        self.window: pyguiforms.Window = pyguiforms.Window("First window", 360.0, 140.0)
        self.name: pyguiforms.TextBox = pyguiforms.TextBox(bounds=(12, 12, 220, 28))
        self.greet: pyguiforms.Button = pyguiforms.Button(text="Greet", bounds=(244, 12, 100, 28))
        self.greeting: pyguiforms.Label = pyguiforms.Label(text="Type a name.", bounds=(12, 56, 332, 28))
        self.window.add(self.name, self.greet, self.greeting)
        self.greet.on("click")(self.on_greet)
        self.window.on("ready")(self.on_ready)

    def on_greet(self, event: pyguiforms.Event) -> None:
        typed: str = str(self.name.text).strip()
        self.greeting.text = "Hello, " + (typed if typed != "" else "stranger") + "."
        print(self.greeting.text, flush=True)
        if self.automatic:
            self.window.close()

    def on_ready(self, event: pyguiforms.Event) -> None:
        if self.automatic:
            self.window.post(self.on_automatic_turn)

    def on_automatic_turn(self, event: pyguiforms.Event) -> None:
        self.name.text = "Ada"
        self.greet.raise_event("click")


def main() -> int:
    greeter: Greeter = Greeter("--auto" in sys.argv)
    with greeter.window:
        greeter.window.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
