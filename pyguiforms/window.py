"""A top-level window: a root panel the library shows and runs (windows.run).

``Window`` keeps its root panel and the controls added to it. ``run``
shows the window and returns when it closes; ``on("ready")``,
``on("closing")`` and ``on("closed")`` subscribe to the run's three
moments (a closing handler may set ``event.cancel = True``; its ``reason``
field says why: "user", "application" or "system"). A handler's exception
closes the window and ``run`` raises it (``native.set_failure_hook`` can
handle it instead). ``post`` runs a function on the UI thread from any
thread; ``close`` asks the window to close, as a program does.
"""

from __future__ import annotations

import typing

from pyguiforms import _controls
from pyguiforms import controls
from pyguiforms import native

RUN_MOMENTS: tuple[str, ...] = ("ready", "closing", "closed")


class HandlerList:
    """The handlers of one run moment, called in the order they subscribed."""

    def __init__(self) -> None:
        self.handlers: list[controls.Handler] = []

    def __call__(self, event: native.Event) -> None:
        for handler in self.handlers:
            handler(event)


class WindowSubscriber:
    """The decorator ``Window.on`` returns."""

    def __init__(self, window: Window, moment: str) -> None:
        self.window: Window = window
        self.moment: str = moment

    def __call__(self, handler: controls.Handler) -> controls.Handler:
        self.window.moments[self.moment].handlers.append(handler)
        return handler


class Window:
    """A window: its title, client size, minimum size and root control (a new panel unless one is given)."""

    def __init__(self, title: str = "", width: float = 640.0, height: float = 480.0, minimum_width: float = 0.0,
                 minimum_height: float = 0.0, stable_id: str | None = None,
                 root: controls.Control | None = None) -> None:
        self.title: str = title
        self.width: float = width
        self.height: float = height
        self.minimum_width: float = minimum_width
        self.minimum_height: float = minimum_height
        self.session: native.Session = native.session()
        # The control the run makes a window for: a new panel, or one given
        # (a form document's root control).
        self.root: controls.Control = root if root is not None else _controls.Panel(stable_id)
        self.moments: dict[str, HandlerList] = {}
        for moment in RUN_MOMENTS:
            self.moments[moment] = HandlerList()
        self.running: bool = False

    def add(self, *children: controls.Control) -> None:
        """Appends children to the root panel."""
        self.root.add(*children)

    @property
    def children(self) -> tuple[controls.Control, ...]:
        return self.root.children

    def on(self, moment: str) -> typing.Callable[[controls.Handler], controls.Handler]:
        """A decorator for "ready", "closing" or "closed"."""
        if moment not in RUN_MOMENTS:
            raise ValueError("a window's run has no moment " + repr(moment) + "; it has " + ", ".join(RUN_MOMENTS))
        return WindowSubscriber(self, moment)

    def handler(self, moment: str) -> HandlerList | None:
        handlers: HandlerList = self.moments[moment]
        if len(handlers.handlers) == 0:
            return None
        return handlers

    def run(self) -> None:
        """Shows the window and returns when it closes; a handler's failure closes it and is raised here."""
        self.running = True
        try:
            self.session.run(self.root.identity, self.title, self.width, self.height, self.minimum_width,
                             self.minimum_height, self.handler("ready"), self.handler("closing"),
                             self.handler("closed"))
        finally:
            self.running = False

    def close(self) -> None:
        """Asks the running window to close; its closing handlers see the reason "application"."""
        self.session.request_close(self.root.identity)

    def post(self, handler: controls.Handler) -> None:
        """Runs handler on the UI thread, from any thread (dispatch.begin_invoke)."""
        self.session.begin_invoke(self.root.identity, handler)

    def release(self) -> None:
        self.root.release()

    def __enter__(self) -> Window:
        return self

    def __exit__(self, *unused_exception: object) -> None:
        self.root.dispose()
        self.root.release()
