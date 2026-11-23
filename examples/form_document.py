"""A window from a form document, bound to a model, with a theme sheet and model tools.

    GUI_FORMS_ABI_LIBRARY=/path/to/libgui_forms_abi.1.dylib python3 examples/form_document.py [--auto] [--mcp]

``forms/settings.form`` describes the window; the program loads it with
its model (two ``pyguiforms.Value`` objects), loads ``forms/settings.theme.css``
and attaches the behaviour: OK reports the setting and closes. With --auto
a model-tools client on another thread checks the box, clicks OK through
the tools and the window closes. With --mcp the window also answers MCP
requests on stdin and stdout (so the example reports on stderr).
"""

from __future__ import annotations

import pathlib
import sys
import threading

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import pyguiforms  # noqa: E402

HERE: pathlib.Path = pathlib.Path(__file__).resolve().parent


class Settings:
    """The model the document binds: its attributes are the Values bind's to names."""

    def __init__(self) -> None:
        self.autosave: pyguiforms.Value = pyguiforms.Value(False)


class SettingsWindow:
    """The loaded form and its behaviour."""

    def __init__(self, settings: Settings) -> None:
        self.settings: Settings = settings
        pyguiforms.themes.load_sheet((HERE / "forms" / "settings.theme.css").read_text(encoding="utf-8"),
                                     "settings")
        self.form: pyguiforms.Form = pyguiforms.load_form(HERE / "forms" / "settings.form", model=settings)
        self.form.settings_ok.on("click")(self.on_ok)
        self.tools: pyguiforms.automation.ModelTools = pyguiforms.automation.ModelTools(self.form.window)

    def on_ok(self, event: pyguiforms.Event) -> None:
        print("autosave is", self.settings.autosave.value, file=sys.stderr, flush=True)
        self.form.window.close()


class ToolClient:
    """Drives the window through the model tools from its own thread, as an agent would."""

    def __init__(self, tools: pyguiforms.automation.ModelTools) -> None:
        self.tools: pyguiforms.automation.ModelTools = tools

    def run(self) -> None:
        print("tree:", self.tools.call("describe", {}), file=sys.stderr, flush=True)
        self.tools.call("set_property", {"id": "settings.autosave", "name": "checked", "value": True})
        self.tools.call("invoke", {"id": "settings.ok", "interaction": "click"})


def main() -> int:
    settings: Settings = Settings()
    window: SettingsWindow = SettingsWindow(settings)
    if "--mcp" in sys.argv:
        pyguiforms.automation.serve_stdio(window.tools)
    client: threading.Thread | None = None
    if "--auto" in sys.argv:
        client = threading.Thread(target=ToolClient(window.tools).run, name="tool-client")
        window.form.window.on("ready")(StartClient(client))
    with window.form:
        window.form.run()
    if client is not None:
        client.join()
    return 0


class StartClient:
    """Starts the tool client once the window is ready."""

    def __init__(self, client: threading.Thread) -> None:
        self.client: threading.Thread = client

    def __call__(self, event: pyguiforms.Event) -> None:
        self.client.start()


if __name__ == "__main__":
    sys.exit(main())
