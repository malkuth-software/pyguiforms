"""The study's prototype on the stage-2 API: one window, one button, one click callback.

    GUI_FORMS_ABI_LIBRARY=/path/to/libgui_forms_abi.1.dylib python3 examples/one_button.py [--auto] [--fail]

Without --auto the window waits for a person to click the button; the click
closes it. With --auto the ready handler posts (Window.post) a function that
raises the button's click through Control::on_click's base
(Component.raise_event), the path a person's click takes from the raiser
on. With --fail the click handler raises, to show the failure crossing back
as a Python exception from run() instead of unwinding through C. A watchdog
thread posts a close after 20 seconds from off the UI thread, so the
prototype always ends.
"""

from __future__ import annotations

import pathlib
import sys
import threading

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import pyguiforms  # noqa: E402
from pyguiforms import native  # noqa: E402


class Prototype:
    """The window, its button and what the handlers saw."""

    def __init__(self, auto_click: bool, fail_in_click: bool) -> None:
        self.auto_click: bool = auto_click
        self.fail_in_click: bool = fail_in_click
        self.clicks: int = 0
        self.window: pyguiforms.Window = pyguiforms.Window("pyguiforms prototype", 320.0, 120.0,
                                                           stable_id="prototype.root")
        self.button: pyguiforms.Button = pyguiforms.Button("prototype.ok-button", text="Click me",
                                                           bounds=(24, 24, 160, 36))
        self.window.add(self.button)
        self.button.on("click")(self.on_click)
        self.window.on("ready")(self.on_ready)
        self.window.on("closing")(self.on_closing)
        self.window.on("closed")(self.on_closed)

    def on_click(self, event: pyguiforms.Event) -> None:
        self.clicks += 1
        print("click: event", repr(event.name), "sender", hex(event.sender), "count", self.clicks, flush=True)
        if self.fail_in_click:
            raise ValueError("the click handler failed on purpose")
        self.window.close()

    def on_ready(self, event: pyguiforms.Event) -> None:
        print("ready: event", repr(event.name), "sender", hex(event.sender), flush=True)
        if self.auto_click:
            self.window.post(self.on_posted_click)

    def on_posted_click(self, event: pyguiforms.Event) -> None:
        print("posted: on thread", threading.current_thread().name, flush=True)
        self.button.raise_event("click")

    def on_closing(self, event: pyguiforms.Event) -> None:
        print("closing: reason", event.field("reason"), flush=True)

    def on_closed(self, event: pyguiforms.Event) -> None:
        print("closed: reason", event.field("reason"), flush=True)

    def on_watchdog_close(self, event: pyguiforms.Event) -> None:
        print("watchdog: closing the window", flush=True)
        self.window.close()

    def watchdog(self, stop: threading.Event) -> None:
        if stop.wait(20.0):
            return
        self.window.post(self.on_watchdog_close)


def main() -> int:
    prototype: Prototype = Prototype("--auto" in sys.argv, "--fail" in sys.argv)
    print(prototype.window.session.version(), "from", prototype.window.session.library.path.name, flush=True)
    stop: threading.Event = threading.Event()
    watchdog: threading.Thread = threading.Thread(target=prototype.watchdog, args=(stop,), name="watchdog")
    watchdog.start()
    result: int = 0
    try:
        with prototype.window:
            prototype.window.run()
        print("run returned; clicks", prototype.clicks, flush=True)
    except native.CallbackFailure as failure:
        print("run raised CallbackFailure:", failure, "| cause:", repr(failure.thrown), flush=True)
        result = 3
    finally:
        stop.set()
        watchdog.join()
    prototype.button.release()
    print("pending callbacks run:", prototype.window.session.run_pending(), "| handlers still lent:",
          native.registry.live_count(), flush=True)
    return result


if __name__ == "__main__":
    sys.exit(main())
