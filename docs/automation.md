# Model tools and MCP

`pyguiforms.automation` offers a running window's controls as tools: for a
language model, for a test driver, or for any client that speaks the
Model Context Protocol. Controls are addressed by stable ID.

```python
from pyguiforms import automation

tools = automation.ModelTools(window)
automation.serve_stdio(tools)       # MCP on stdin and stdout
window.run()
```

## The tools

| Tool | Arguments | Result |
|---|---|---|
| `describe` | none | the control tree: each object's `id`, `type`, `text` and `children` |
| `list_properties` | `id` | each property's `name`, `kind` and whether it is `writable` |
| `get_property` | `id`, `name` | the value (geometry and fonts as objects of their fields) |
| `set_property` | `id`, `name`, `value` | the value read back; geometry as a list (`bounds`: x, y, width, height), an enumeration by its choice's name |
| `invoke` | `id`, `interaction` | raises the interaction as the library would (`click`) |

- `tools.definitions()` lists the tools with JSON Schemas, in the shape
  model APIs take for tool use.
- `tools.call(name, arguments)` runs one and returns a JSON-ready result.
- A refused call (an unknown ID, property or interaction, or a bad
  argument) raises `automation.ToolError`.
- Components a window does not hold, such as a form's commands, are
  passed as `ModelTools(window, form.objects)`.

## Threads

A tool may be called from any thread. Off the UI thread the call is posted
to it and waited for, so controls are only touched on the UI thread. A call
fails after `CALL_TIMEOUT_SECONDS` (10 s) when the window is not running.

## MCP

`McpServer` answers `initialize`, `ping`, `tools/list` and `tools/call`
(JSON-RPC 2.0). `serve_stdio` runs it on a daemon thread, one JSON message
per line. While it runs, stdout belongs to the protocol, so the program
writes its own output to stderr.

`examples/form_document.py --mcp` is a complete server. A client that
launches servers from a configuration starts it like this:

```json
{
  "mcpServers": {
    "settings-window": {
      "command": "python3",
      "args": ["examples/form_document.py", "--mcp"]
    }
  }
}
```
