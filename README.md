# The Poor Man's Apple Intelligence

This is a Python-based Model Context Protocol (MCP) server that exposes a suite of tools which allows Claude (or any other model supporting MCPs) to do things that Apple Intelligence can (and some things that it can't!) via Shortcuts.

![Demo](demo.gif)

Each tool corresponds to a function in the given shortcut (e.g., sending messages, making calls, managing calendar events). Under the hood, the server builds a four-line payload, pipes it into the `shortcuts` CLI, and returns the shortcut’s response which is then given back to Claude.

### Complete list of features:

* Send text messages via iMessage
* Call a contact
* Facetime a contact
* Send an email
* Retrieve all contacts (context for Claude)
* List past calendar events (context for Claude)
* List future calendar events (context for Claude)
* List calendar events today (context for Claude)
* Create a new calendar event
* List all pending reminders (context for Claude)
* Create a reminder
* Fetch the current weather
* Fetch the weather forecast
* Set an alarm at a specified time
* Delete an existing alarm
* List all configured alarms

---

## Table of Contents

* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Integrating with Claude for Desktop](#integrating-with-claude-for-desktop)
* [How It Works](#how-it-works)
  * [Server Structure](#server-structure)
  * [Building the Payload](#building-the-payload)
  * [Piping into `shortcuts` CLI](#piping-into-shortcuts-cli)
  * [Shortcut-side Splitting](#shortcut-side-splitting)
* [Running Locally](#running-locally)
* [License](#license)

---

## Prerequisites

* **macOS** (the `shortcuts` CLI ships with macOS Monterey and later)
* **Python 3.8+**
* **uv CLI** (for dependency management)
* **MCP Python SDK**

---

## Installation

1. **Clone this repo**

   ```bash
   git clone https://github.com/nathan-barry/poor-mans-apple-intelligence.git
   cd poor-mans-apple-intelligence
   ```

2. **Install dependencies**:

   ```bash
   uv sync
   ```

3. **Add the two shortcuts**:

   ```bash
   open getcontact.shortcut # helper function
   open switch.shortcut     # meat and potatoes
   ```

---

## Integrating with Claude for Desktop

In `claude_desktop_config.json` (find this by following [this guide](https://modelcontextprotocol.io/quickstart/user)):

```json
{
  "mcpServers": {
    "shortcutRunner": {
      "command": "bash",
      "args": [
        "-lc",
        "cd /path/to/poor-mans-apple-intelligence && uv run mcp run server.py"
      ]
    }
  }
}
```

Restart Claude, click the 🔨 icon, and pick `shortcutRunner`. It will ask for permission before each action.

---

## How It Works

### Server Structure
This server defines:

#### Command Dataclass

```python
@dataclass
class Command:
    function: str
    arg_1: str = ""
    arg_2: str = ""
    arg_3: str = ""

    def payload(self) -> str:
        return "\n".join([self.function, self.arg_1, self.arg_2, self.arg_3]) + "\n"
```

Encapsulates the four fields and provides a `.payload()` method that joins them with newlines.

#### `run_command` Helper

```python
def run_command(cmd: Command) -> str:
    try:
        proc = subprocess.run(
            ["shortcuts", "run", "switch"],
            input=cmd.payload().encode("utf-8"),
            capture_output=True,
            check=True,
        )
        return proc.stdout.decode("utf-8").strip() or "OK"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.decode('utf-8').strip()}"
```

Handles the `subprocess` invocation once, returning either the shortcut’s `stdout` (or `OK` if empty) or the error text.

#### Exposed Tools

Each Shortcut action is exposed as an `@mcp.tool()` with a clear signature. Example:

```python
@mcp.tool()
def sendMessage(name: str, message: str) -> str:
    return run_command(Command("sendMessage", name, message))
```

### Building the Payload

1. **`Command.payload()`** gathers:

   * `function`
   * `arg_1`, `arg_2`, `arg_3` (empty strings by default)
2. **Joins** them with `"\n"` and appends a trailing newline.

### Piping into `shortcuts` CLI

* We spawn:

  ```bash
  shortcuts run switch
  ```
* **Stdin** is fed the 4-line payload.
* **Stdout** is captured and returned to the client.

### Shortcut-side Splitting

In the Apple Shortcut named **`switch`**, the first action should be to:

1. **Get `Text`** from `Shortcut Input` (the piped payload).
2. **Split** that text by newline into a list.
3. **Assign**:

   * `List Item 1` → `function_name`
   * `List Item 2` → `arg_1`
   * `List Item 3` → `arg_2`
   * `List Item 4` → `arg_3`
4. **Run** the switch/case logic on `function_name`, using the args as needed.

---

## Running Locally
In case you want to for some other purpose.

```bash
uv run mcp dev server.py
# (or)
uv run mcp run server.py
```

---

## License

This project is licensed under the MIT License.
