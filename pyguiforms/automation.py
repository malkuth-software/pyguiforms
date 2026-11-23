"""Model tools: a running window's controls, by stable ID, as tools a language model or test client calls.

    tools = pyguiforms.automation.ModelTools(window)
    pyguiforms.automation.serve_stdio(tools)      # an MCP server on stdin and stdout
    window.run()

GUI.Forms' C ABI has no automation surface of its own (its automation
channel is to become an MCP integration, gui_forms
docs/user/hosts-and-capabilities.md), so this module builds one in Python
over the tables the bindings already use:

- ``ModelTools`` offers five tools: ``describe`` (the control tree with
  each object's stable ID, type and text), ``list_properties``,
  ``get_property``, ``set_property`` and ``invoke`` (raise an interaction
  such as ``click`` as the library would). ``definitions()`` lists them
  with JSON Schemas, in the shape model APIs take for tool use, and
  ``call(name, arguments)`` runs one and gives a JSON-ready result.
- ``McpServer`` answers the Model Context Protocol's JSON-RPC messages
  (``initialize``, ``tools/list``, ``tools/call``, ``ping``) for a
  ``ModelTools``; ``serve_stdio`` runs it on a thread over stdin and stdout,
  one JSON message per line.

Threads: a tool may be called from any thread. Off the UI thread the call
is posted to it (Window.post) and waited for, so the controls are only
touched on the UI thread; a call that does not finish within
``CALL_TIMEOUT_SECONDS`` (the window is not running) fails.
"""

from __future__ import annotations

import json
import sys
import threading
import typing

from pyguiforms import controls
from pyguiforms import native
from pyguiforms import values
from pyguiforms import window

CALL_TIMEOUT_SECONDS: float = 10.0
PROTOCOL_VERSION: str = "2025-06-18"
SERVER_NAME: str = "pyguiforms"
SERVER_VERSION: str = "0.1.0"
MAXIMUM_DESCRIBED_OBJECTS: int = 4096


class ToolError(Exception):
    """A tool call the tools refuse: an unknown object, property, interaction or argument."""


def json_ready(value: object) -> object:
    """A property value in JSON's terms: a geometry or font record becomes an object of its fields."""
    as_dictionary: typing.Callable[[], dict] | None = getattr(value, "_asdict", None)
    if as_dictionary is not None:
        return dict(as_dictionary())
    if isinstance(value, (list, tuple)):
        items: list[object] = []
        for item in value:
            items.append(json_ready(item))
        return items
    return value


def from_json(value: object) -> object:
    """A JSON argument as a property value: an object of fields becomes the tuple of its values, in order."""
    if isinstance(value, dict):
        fields: list[object] = []
        for item in value.values():
            fields.append(item)
        return tuple(fields)
    return value


def object_schema(properties: dict[str, dict], required: list[str]) -> dict:
    schema: dict = {"type": "object", "properties": properties, "required": required, "additionalProperties": False}
    return schema


def tool_definitions() -> list[dict]:
    identity: dict = {"type": "string", "description": "the object's stable ID, as describe lists it"}
    name: dict = {"type": "string", "description": "the property's schema name, such as text or enabled"}
    definitions: list[dict] = [
        {"name": "describe",
         "description": "Lists the window's controls as a tree: each object's stable ID, schema type and text.",
         "input_schema": object_schema({}, [])},
        {"name": "list_properties",
         "description": "Lists an object's properties with their kinds and whether they can be written.",
         "input_schema": object_schema({"id": identity}, ["id"])},
        {"name": "get_property",
         "description": "Reads one property of an object.",
         "input_schema": object_schema({"id": identity, "name": name}, ["id", "name"])},
        {"name": "set_property",
         "description": "Writes one property of an object. Geometry is a list of numbers (bounds: x, y, width, "
                        "height); an enumeration is its choice's name.",
         "input_schema": object_schema({"id": identity, "name": name, "value": {}}, ["id", "name", "value"])},
        {"name": "invoke",
         "description": "Raises an interaction of an object as the library would, such as click on a button.",
         "input_schema": object_schema({"id": identity, "interaction": {"type": "string"}}, ["id", "interaction"])},
    ]
    return definitions


class PostedCall:
    """One tool call posted to the UI thread, and its outcome."""

    def __init__(self, tools: ModelTools, name: str, arguments: dict) -> None:
        self.tools: ModelTools = tools
        self.name: str = name
        self.arguments: dict = arguments
        self.done: threading.Event = threading.Event()
        self.result: object = None
        self.failure: BaseException | None = None

    def __call__(self, event: native.Event) -> None:
        try:
            self.result = self.tools.call_here(self.name, self.arguments)
        except BaseException as thrown:
            self.failure = thrown
        finally:
            self.done.set()


class ModelTools:
    """The tools over one window's controls, plus any further components by stable ID (a form's commands)."""

    def __init__(self, target: window.Window, components: dict[str, controls.Component] | None = None) -> None:
        self.window: window.Window = target
        self.components: dict[str, controls.Component] = {} if components is None else dict(components)

    def definitions(self) -> list[dict]:
        """The tools as a model API takes them: name, description and input_schema (JSON Schema)."""
        return tool_definitions()

    def call(self, name: str, arguments: dict) -> object:
        """Runs a tool from any thread and gives its JSON-ready result; raises ToolError for a refused call."""
        session: native.Session = self.window.session
        if threading.current_thread() is session.ui_thread:
            return self.call_here(name, arguments)
        posted: PostedCall = PostedCall(self, name, arguments)
        self.window.post(posted)
        if not posted.done.wait(CALL_TIMEOUT_SECONDS):
            raise ToolError("the window did not answer within " + str(CALL_TIMEOUT_SECONDS) + " s (is it running?)")
        if posted.failure is not None:
            raise posted.failure
        return posted.result

    def call_here(self, name: str, arguments: dict) -> object:
        if not isinstance(arguments, dict):
            raise ToolError("a tool's arguments are an object")
        if name == "describe":
            return self.describe()
        if name == "list_properties":
            return self.list_properties(self.find(arguments))
        if name == "get_property":
            found: controls.Component = self.find(arguments)
            property_name: str = self.text_argument(arguments, "name")
            return json_ready(self.guarded_get(found, property_name))
        if name == "set_property":
            found = self.find(arguments)
            property_name = self.text_argument(arguments, "name")
            if "value" not in arguments:
                raise ToolError("set_property takes a value")
            self.guarded_set(found, property_name, from_json(arguments["value"]))
            return json_ready(self.guarded_get(found, property_name))
        if name == "invoke":
            found = self.find(arguments)
            interaction: str = self.text_argument(arguments, "interaction")
            try:
                found.raise_event(interaction)
            except (ValueError, native.GuiFormsError) as refused:
                raise ToolError(str(refused)) from refused
            return {"invoked": interaction}
        raise ToolError("no tool named " + repr(name))

    @staticmethod
    def text_argument(arguments: dict, name: str) -> str:
        value: object = arguments.get(name)
        if not isinstance(value, str):
            raise ToolError("the argument " + name + " is a string")
        return value

    @staticmethod
    def guarded_get(found: controls.Component, name: str) -> object:
        try:
            value: object = found.get(name)
        except (AttributeError, native.GuiFormsError) as refused:
            raise ToolError(str(refused)) from refused
        return value

    @staticmethod
    def guarded_set(found: controls.Component, name: str, value: object) -> None:
        try:
            found.set(name, value)
        except (AttributeError, ValueError, TypeError, native.GuiFormsError) as refused:
            raise ToolError(str(refused)) from refused

    def objects(self) -> dict[str, controls.Component]:
        """Every object the tools reach, by stable ID: the window's control tree and the components given."""
        found: dict[str, controls.Component] = dict(self.components)
        pending: list[controls.Control] = [self.window.root]
        while len(pending) > 0 and len(found) < MAXIMUM_DESCRIBED_OBJECTS:
            control: controls.Control = pending.pop()
            found[control.stable_id] = control
            pending.extend(control.children)
        return found

    def find(self, arguments: dict) -> controls.Component:
        identity: str = self.text_argument(arguments, "id")
        found: controls.Component | None = self.objects().get(identity)
        if found is None or found.identity == 0:
            raise ToolError("no object with the stable ID " + repr(identity))
        return found

    def describe_one(self, found: controls.Component) -> dict:
        described: dict = {"id": found.stable_id, "type": found.TYPE_ID}
        if "text" in found.type_info.properties:
            described["text"] = found.get("text")
        children: list[dict] = []
        if isinstance(found, controls.Control):
            for child in found.children:
                children.append(self.describe_one(child))
        if len(children) > 0:
            described["children"] = children
        return described

    def describe(self) -> dict:
        components: list[dict] = []
        for found in self.components.values():
            if not isinstance(found, controls.Control):
                components.append({"id": found.stable_id, "type": found.TYPE_ID})
        described: dict = {"title": self.window.title, "root": self.describe_one(self.window.root)}
        if len(components) > 0:
            described["components"] = components
        return described

    @staticmethod
    def list_properties(found: controls.Component) -> list[dict]:
        listed: list[dict] = []
        for info in found.type_info.properties.values():
            listed.append({"name": info.name, "kind": KIND_WORDS.get(info.kind, str(info.kind)),
                           "writable": info.writable()})
        return listed


def kind_words() -> dict[int, str]:
    words: dict[int, str] = {}
    for word, kind in values.KIND_NAMES.items():
        words[kind] = word
    return words


KIND_WORDS: dict[int, str] = kind_words()


# ---------------------------------------------------------------------- MCP


class McpServer:
    """Answers MCP JSON-RPC messages for one ModelTools (tools only)."""

    def __init__(self, tools: ModelTools) -> None:
        self.tools: ModelTools = tools

    @staticmethod
    def reply(identity: object, result: dict) -> dict:
        return {"jsonrpc": "2.0", "id": identity, "result": result}

    @staticmethod
    def error(identity: object, code: int, message: str) -> dict:
        return {"jsonrpc": "2.0", "id": identity, "error": {"code": code, "message": message}}

    def mcp_tools(self) -> list[dict]:
        listed: list[dict] = []
        for definition in self.tools.definitions():
            listed.append({"name": definition["name"], "description": definition["description"],
                           "inputSchema": definition["input_schema"]})
        return listed

    def handle(self, message: object) -> dict | None:
        """The reply to one message; None for a notification."""
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"),
                                                                                               str):
            identity: object = message.get("id") if isinstance(message, dict) else None
            return self.error(identity, -32600, "not a JSON-RPC 2.0 request")
        method: str = message["method"]
        if "id" not in message:
            return None
        identity = message["id"]
        parameters: object = message.get("params", {})
        if not isinstance(parameters, dict):
            return self.error(identity, -32602, "params is an object")
        if method == "initialize":
            requested: object = parameters.get("protocolVersion")
            version: str = requested if isinstance(requested, str) else PROTOCOL_VERSION
            return self.reply(identity, {"protocolVersion": version, "capabilities": {"tools": {}},
                                         "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}})
        if method == "ping":
            return self.reply(identity, {})
        if method == "tools/list":
            return self.reply(identity, {"tools": self.mcp_tools()})
        if method == "tools/call":
            return self.call(identity, parameters)
        return self.error(identity, -32601, "no method " + method)

    def call(self, identity: object, parameters: dict) -> dict:
        name: object = parameters.get("name")
        arguments: object = parameters.get("arguments", {})
        if not isinstance(name, str):
            return self.error(identity, -32602, "tools/call names its tool")
        try:
            result: object = self.tools.call(name, arguments if isinstance(arguments, dict) else None)
        except ToolError as refused:
            return self.reply(identity, {"content": [{"type": "text", "text": str(refused)}], "isError": True})
        text: str = json.dumps(result, ensure_ascii=False)
        return self.reply(identity, {"content": [{"type": "text", "text": text}], "isError": False})


class StdioServer:
    """Reads one JSON message per line from a stream and writes each reply as one line."""

    def __init__(self, server: McpServer, reader: typing.TextIO, writer: typing.TextIO) -> None:
        self.server: McpServer = server
        self.reader: typing.TextIO = reader
        self.writer: typing.TextIO = writer
        self.write_lock: threading.Lock = threading.Lock()

    def answer(self, line: str) -> None:
        reply: dict | None
        try:
            message: object = json.loads(line)
        except ValueError:
            reply = McpServer.error(None, -32700, "not JSON")
        else:
            reply = self.server.handle(message)
        if reply is None:
            return
        with self.write_lock:
            self.writer.write(json.dumps(reply, ensure_ascii=False) + "\n")
            self.writer.flush()

    def serve(self) -> None:
        for line in self.reader:
            if line.strip() == "":
                continue
            self.answer(line)


def serve_stdio(tools: ModelTools, reader: typing.TextIO | None = None,
                writer: typing.TextIO | None = None) -> threading.Thread:
    """Starts an MCP server for tools on a daemon thread over stdin and stdout (or the streams given)."""
    server: StdioServer = StdioServer(McpServer(tools), reader if reader is not None else sys.stdin,
                                      writer if writer is not None else sys.stdout)
    thread: threading.Thread = threading.Thread(target=server.serve, name="pyguiforms-mcp", daemon=True)
    thread.start()
    return thread
