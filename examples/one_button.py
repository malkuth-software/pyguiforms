#!/usr/bin/env python3
"""The study's prototype: one window, one button, one click callback, end to end.

    GUI_FORMS_ABI_LIBRARY=/path/to/libgui_forms_abi.1.dylib python3 examples/one_button.py [--auto] [--fail]

Without --auto the window waits for a person to click the button; the click
closes it. With --auto the ready callback posts (dispatch.begin_invoke) a
callback that raises the button's click through Control::on_click's base
(classes.base_raiser), the path a person's click takes from the raiser on.
With --fail the click handler raises, to show the failure crossing back as a
Python exception from run() instead of unwinding through C. A watchdog
thread posts a close after 20 seconds from off the UI thread, so the
prototype always ends.
"""

from __future__ import annotations

import pathlib
import sys
import threading

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pyguiforms import native  # noqa: E402


class Prototype:
    """The window's objects and what the callbacks saw."""

    def __init__(self, session: native.Session, auto_click: bool, fail_in_click: bool) -> None:
        self.session: native.Session = session
        self.auto_click: bool = auto_click
        self.fail_in_click: bool = fail_in_click
        self.clicks: int = 0
        self.root: native.ObjectReference = session.create("panel", "prototype.root")
        # Made from a class table (with no overrides) so that its click raiser
        # has a base the auto click can run (classes.base_raiser).
        self.button: native.ObjectReference = session.create_from_class("gf_button_class", native._abi.GF_CLASS_BUTTON,
                                                                        "prototype.ok-button")
        session.set_text(self.button, "text", "Click me")
        session.set_rectangle(self.button, "bounds", 24.0, 24.0, 160.0, 36.0)
        session.insert_child(self.root, self.button, 0)
        self.click_subscription: native.Subscription = session.subscribe(self.button, "click", self.on_click)

    def on_click(self, event: native.Event) -> None:
        self.clicks += 1
        print("click: event", repr(event.name()), "sender", hex(event.sender()), "count", self.clicks, flush=True)
        if self.fail_in_click:
            raise ValueError("the click handler failed on purpose")
        self.session.request_close()

    def on_ready(self, event: native.Event) -> None:
        print("ready: event", repr(event.name()), "sender", hex(event.sender()), flush=True)
        if self.auto_click:
            self.session.begin_invoke(self.button, self.on_posted_click)

    def on_posted_click(self, event: native.Event) -> None:
        print("posted: event", repr(event.name()), "on thread", threading.current_thread().name, flush=True)
        self.session.raise_click(self.button)

    def on_closing(self, event: native.Event) -> None:
        print("closing: reason", event.field_text("reason"), flush=True)

    def on_closed(self, event: native.Event) -> None:
        print("closed: reason", event.field_text("reason"), flush=True)

    def on_watchdog_close(self, event: native.Event) -> None:
        print("watchdog: closing the window", flush=True)
        self.session.request_close()

    def watchdog(self, stop: threading.Event) -> None:
        if stop.wait(20.0):
            return
        self.session.begin_invoke(self.root, self.on_watchdog_close)

    def release(self) -> None:
        self.click_subscription.disconnect()
        self.button.release()
        self.root.release()


def main() -> int:
    auto_click: bool = "--auto" in sys.argv
    fail_in_click: bool = "--fail" in sys.argv
    session: native.Session = native.open_session()
    print(session.version(), "from", session.library.path.name, flush=True)
    prototype: Prototype = Prototype(session, auto_click, fail_in_click)
    stop: threading.Event = threading.Event()
    watchdog: threading.Thread = threading.Thread(target=prototype.watchdog, args=(stop,), name="watchdog")
    watchdog.start()
    result: int = 0
    try:
        session.run(prototype.root, "pyguiforms prototype", 320.0, 120.0, prototype.on_ready, prototype.on_closing,
                    prototype.on_closed)
        print("run returned; clicks", prototype.clicks, flush=True)
    except native.CallbackFailure as failure:
        print("run raised CallbackFailure:", failure, "| cause:", repr(failure.thrown), flush=True)
        result = 3
    finally:
        stop.set()
        watchdog.join()
    prototype.release()
    print("pending callbacks run:", session.run_pending(), "| handlers still lent:", native.registry.live_count(),
          flush=True)
    return result


if __name__ == "__main__":
    sys.exit(main())
