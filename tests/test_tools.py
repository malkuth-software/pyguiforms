"""Themes and model tools. The MCP protocol layer needs no library; the rest runs against a real one."""

from __future__ import annotations

import io
import json
import threading
import unittest

import pyguiforms
from pyguiforms import automation
from pyguiforms import native
from pyguiforms import themes

LIBRARY_PRESENT: bool = native.find_library().is_file()


class EchoTools:
    """A stand-in for ModelTools: one tool that echoes its arguments, one that refuses."""

    def definitions(self) -> list[dict]:
        return automation.tool_definitions()

    def call(self, name: str, arguments: dict | None) -> object:
        if name == "describe":
            return {"echo": arguments}
        raise automation.ToolError("refused " + name)


class McpTests(unittest.TestCase):

    def setUp(self) -> None:
        self.server: automation.McpServer = automation.McpServer(EchoTools())

    def test_initialize_and_list(self) -> None:
        reply: dict | None = self.server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                                                 "params": {"protocolVersion": "2025-06-18"}})
        assert reply is not None
        self.assertEqual(reply["result"]["protocolVersion"], "2025-06-18")
        self.assertIn("tools", reply["result"]["capabilities"])
        self.assertIsNone(self.server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        listed: dict | None = self.server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        assert listed is not None
        names: list[str] = []
        for tool in listed["result"]["tools"]:
            names.append(tool["name"])
            self.assertEqual(tool["inputSchema"]["type"], "object")
        self.assertEqual(names, ["describe", "list_properties", "get_property", "set_property", "invoke"])

    def test_calls_and_refusals(self) -> None:
        reply: dict | None = self.server.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                                                 "params": {"name": "describe", "arguments": {"a": 1}}})
        assert reply is not None
        self.assertFalse(reply["result"]["isError"])
        self.assertEqual(json.loads(reply["result"]["content"][0]["text"]), {"echo": {"a": 1}})
        refused: dict | None = self.server.handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                                                   "params": {"name": "invoke", "arguments": {}}})
        assert refused is not None
        self.assertTrue(refused["result"]["isError"])
        unknown: dict | None = self.server.handle({"jsonrpc": "2.0", "id": 5, "method": "nothing"})
        assert unknown is not None
        self.assertEqual(unknown["error"]["code"], -32601)
        self.assertEqual(self.server.handle([1, 2])["error"]["code"], -32600)

    def test_stdio_lines(self) -> None:
        reader: io.StringIO = io.StringIO('{"jsonrpc": "2.0", "id": 7, "method": "ping"}\nnot json\n\n')
        writer: io.StringIO = io.StringIO()
        automation.serve_stdio(EchoTools(), reader, writer).join(5.0)
        lines: list[str] = writer.getvalue().splitlines()
        self.assertEqual(json.loads(lines[0]), {"jsonrpc": "2.0", "id": 7, "result": {}})
        self.assertEqual(json.loads(lines[1])["error"]["code"], -32700)


class ToolScript:
    """A window whose button a tool client on another thread clicks; the click closes the window."""

    def __init__(self) -> None:
        self.window: pyguiforms.Window = pyguiforms.Window("tools", 240.0, 100.0, stable_id="tools.root")
        self.button: pyguiforms.Button = pyguiforms.Button("tools.ok", text="OK", bounds=(8, 8, 80, 28))
        self.window.add(self.button)
        self.tools: automation.ModelTools = automation.ModelTools(self.window)
        self.button.on("click")(self.clicked)
        self.window.on("ready")(self.ready)
        self.client: threading.Thread = threading.Thread(target=self.drive, name="tool-client")
        self.seen: dict[str, object] = {}
        self.failure: BaseException | None = None
        self.clicks: int = 0

    def ready(self, event: native.Event) -> None:
        self.client.start()

    def clicked(self, event: native.Event) -> None:
        self.clicks += 1
        self.window.close()

    def drive(self) -> None:
        try:
            self.seen["tree"] = self.tools.call("describe", {})
            self.seen["set"] = self.tools.call("set_property", {"id": "tools.ok", "name": "bounds",
                                                                "value": [10, 12, 90, 30]})
            self.seen["text"] = self.tools.call("get_property", {"id": "tools.ok", "name": "text"})
            try:
                self.tools.call("get_property", {"id": "tools.none", "name": "text"})
            except automation.ToolError as refused:
                self.seen["refused"] = str(refused)
            self.tools.call("invoke", {"id": "tools.ok", "interaction": "click"})
        except BaseException as thrown:
            self.failure = thrown
            self.window.post(self.close)

    def close(self, event: native.Event) -> None:
        self.window.close()


@unittest.skipUnless(LIBRARY_PRESENT, "no gui_forms_abi1 library (set GUI_FORMS_ABI_LIBRARY)")
class LibraryToolTests(unittest.TestCase):

    def test_a_sheet_loads_and_a_bad_one_is_refused(self) -> None:
        try:
            warnings: list[themes.Finding] = themes.load_sheet(".note { font-size: 13px; }", "test-sheet")
            self.assertEqual(warnings, [])
            self.assertEqual(themes.theme_id(), "test-sheet")
            with self.assertRaises(themes.ThemeError) as refused:
                themes.load_sheet(".note { font-size: ", "broken")
            self.assertGreater(len(refused.exception.findings), 0)
            self.assertEqual(refused.exception.findings[0].severity, "error")
            self.assertEqual(themes.theme_id(), "test-sheet")
        finally:
            themes.reset()

    def test_published_values(self) -> None:
        themes.publish_value("test-gap", 6.0)
        self.assertEqual(themes.published_value("test-gap"), 6.0)
        themes.withdraw_value("test-gap")
        self.assertIsNone(themes.published_value("test-gap"))

    def test_model_tools_drive_a_running_window_from_another_thread(self) -> None:
        script: ToolScript = ToolScript()
        with script.window:
            script.window.run()
        script.client.join(10.0)
        self.assertIsNone(script.failure)
        self.assertEqual(script.clicks, 1)
        tree: dict = script.seen["tree"]
        self.assertEqual(tree["root"]["id"], "tools.root")
        self.assertEqual(tree["root"]["children"][0], {"id": "tools.ok", "type": "button", "text": "OK"})
        self.assertEqual(script.seen["set"], {"x": 10.0, "y": 12.0, "width": 90.0, "height": 30.0})
        self.assertEqual(script.seen["text"], "OK")
        self.assertIn("tools.none", script.seen["refused"])
        script.button.release()


if __name__ == "__main__":
    unittest.main()
