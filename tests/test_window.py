"""The Pythonic layer against a real gui_forms_abi1 (GUI_FORMS_ABI_LIBRARY, or a wheel's copy); skipped without one.

Each window is closed by the test itself, and a watchdog thread posts a
close after 20 seconds, so a lost callback fails the test instead of
hanging it.
"""

from __future__ import annotations

import threading
import unittest

import pyguiforms
from pyguiforms import native
from pyguiforms import values

LIBRARY_PRESENT: bool = native.find_library().is_file()


class Watchdog:
    """Posts a close to window after a time limit, from its own thread, unless stopped first."""

    def __init__(self, window: pyguiforms.Window, seconds: float) -> None:
        self.window: pyguiforms.Window = window
        self.seconds: float = seconds
        self.stop: threading.Event = threading.Event()
        self.fired: bool = False
        self.thread: threading.Thread = threading.Thread(target=self.watch, name="watchdog")

    def watch(self) -> None:
        if self.stop.wait(self.seconds):
            return
        self.fired = True
        self.window.post(self.close)

    def close(self, event: native.Event) -> None:
        self.window.close()

    def __enter__(self) -> Watchdog:
        self.thread.start()
        return self

    def __exit__(self, *unused_exception: object) -> None:
        self.stop.set()
        self.thread.join()


class ClickScript:
    """A window with one button: ready posts a click, the click closes the window, closing records the reason."""

    def __init__(self, fail_in_click: bool) -> None:
        self.window: pyguiforms.Window = pyguiforms.Window("pyguiforms test", 320.0, 120.0)
        self.button: pyguiforms.Button = pyguiforms.Button(text="Close", bounds=(24, 24, 120, 32))
        self.window.add(self.button)
        self.fail_in_click: bool = fail_in_click
        self.clicks: int = 0
        self.reasons: list[object] = []
        self.closed: int = 0
        self.button.on("click")(self.clicked)
        self.window.on("ready")(self.ready)
        self.window.on("closing")(self.closing)
        self.window.on("closed")(self.on_closed)

    def ready(self, event: native.Event) -> None:
        self.window.post(self.click)

    def click(self, event: native.Event) -> None:
        self.button.raise_event("click")

    def clicked(self, event: native.Event) -> None:
        self.clicks += 1
        if self.fail_in_click and self.clicks == 1:
            raise ValueError("the click handler failed on purpose")
        self.window.close()

    def closing(self, event: native.Event) -> None:
        self.reasons.append(event.field("reason"))

    def on_closed(self, event: native.Event) -> None:
        self.closed += 1

    def release(self) -> None:
        self.window.root.dispose()
        self.button.release()
        self.window.release()


class CarryOn:
    """A failure hook that handles every failure and keeps them."""

    def __init__(self) -> None:
        self.failures: list[native.CallbackFailure] = []

    def __call__(self, failure: native.CallbackFailure) -> bool:
        self.failures.append(failure)
        return True


class ThreadAttempt:
    """Tries a UI call from another thread and keeps what it raised."""

    def __init__(self, button: pyguiforms.Button) -> None:
        self.button: pyguiforms.Button = button
        self.raised: BaseException | None = None

    def __call__(self) -> None:
        try:
            self.button.text = "from another thread"
        except BaseException as thrown:
            self.raised = thrown


@unittest.skipUnless(LIBRARY_PRESENT, "no gui_forms_abi1 library (set GUI_FORMS_ABI_LIBRARY)")
class WindowTests(unittest.TestCase):

    def test_properties_round_trip(self) -> None:
        with pyguiforms.Button(text="OK", bounds=(1, 2, 30, 40)) as button:
            self.assertEqual(button.text, "OK")
            self.assertEqual(button.bounds, values.Rect(1.0, 2.0, 30.0, 40.0))
            button.enabled = False
            self.assertIs(button.enabled, False)
            button.text_alignment = "top_left"
            self.assertEqual(button.text_alignment, "top_left")
            button.reset("text")
            self.assertEqual(button.text, "")

    def test_an_unknown_choice_or_property_is_refused(self) -> None:
        with pyguiforms.Button() as button:
            with self.assertRaises(ValueError):
                button.text_alignment = "nowhere"
            with self.assertRaises(AttributeError):
                button.set("no_such_property", 1)
            with self.assertRaises(ValueError):
                button.on("no_such_interaction")

    def test_a_click_runs_its_handler_and_the_close_reports_its_reason(self) -> None:
        script: ClickScript = ClickScript(False)
        with Watchdog(script.window, 20.0) as watchdog:
            script.window.run()
        self.assertFalse(watchdog.fired)
        self.assertEqual(script.clicks, 1)
        self.assertEqual(script.closed, 1)
        # gf_abi.h: a program's close reports "application"; builds before
        # gui_forms branch claude/abi-close-reason report "user" on macOS.
        self.assertEqual(len(script.reasons), 1)
        self.assertIn(script.reasons[0], ("application", "user"))
        script.release()

    def test_a_handler_failure_closes_the_window_and_run_raises_it(self) -> None:
        script: ClickScript = ClickScript(True)
        with Watchdog(script.window, 20.0) as watchdog:
            with self.assertRaises(native.CallbackFailure) as raised:
                script.window.run()
        self.assertFalse(watchdog.fired)
        self.assertIsInstance(raised.exception.thrown, ValueError)
        self.assertEqual(script.clicks, 1)
        script.release()

    def test_a_failure_hook_that_handles_the_failure_carries_on(self) -> None:
        script: ClickScript = ClickScript(True)
        hook: CarryOn = CarryOn()
        native.set_failure_hook(hook)
        try:
            script.window.on("ready")(script.ready)
            with Watchdog(script.window, 20.0) as watchdog:
                script.window.run()
        finally:
            native.set_failure_hook(None)
        self.assertFalse(watchdog.fired)
        self.assertEqual(len(hook.failures), 1)
        self.assertEqual(script.clicks, 2)
        script.release()

    def test_ui_calls_from_another_thread_are_refused(self) -> None:
        with pyguiforms.Button() as button:
            attempt: ThreadAttempt = ThreadAttempt(button)
            thread: threading.Thread = threading.Thread(target=attempt)
            thread.start()
            thread.join()
            self.assertIsInstance(attempt.raised, native.WrongThreadError)

    def test_children_and_layout(self) -> None:
        with pyguiforms.Panel() as panel:
            first: pyguiforms.Label = pyguiforms.Label(text="one")
            second: pyguiforms.Label = pyguiforms.Label(text="two")
            with panel.layout_suspended():
                panel.add(first, second)
            self.assertEqual(panel.children, (first, second))
            self.assertEqual(panel.session.child_count(panel.identity), 2)
            panel.remove(first)
            self.assertEqual(panel.session.child_count(panel.identity), 1)
            first.release()
            second.release()

    def test_handlers_are_released_with_their_objects(self) -> None:
        session: native.Session = native.session()
        session.run_pending()
        before: int = native.registry.live_count()
        button: pyguiforms.Button = pyguiforms.Button()
        button.on("click")(ignore_event)
        button.on_change("text")(ignore_event)
        self.assertEqual(native.registry.live_count(), before + 2)
        button.dispose()
        button.release()
        session.run_pending()
        self.assertEqual(native.registry.live_count(), before)


def ignore_event(event: native.Event) -> None:
    pass


if __name__ == "__main__":
    unittest.main()
