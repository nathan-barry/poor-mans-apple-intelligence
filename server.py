import subprocess
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Create your MCP server
mcp = FastMCP("ShortcutRunner")


@mcp.tool()
def run_switch(
    action: str,
    param1: Optional[str] = "",
    param2: Optional[str] = "",
    param3: Optional[str] = ""
) -> str:
    """
    Invoke the 'switch' Apple Shortcut with a 4-line payload:
      1) action (e.g. sendMessage, signalCall, etc.)
      2) param1
      3) param2
      4) param3

    Returns the stdout (or stderr on failure) from the 'shortcuts' command.
    """
    # Build the 4-line input for the shortcut
    payload = "\n".join(
        [action, param1 or "", param2 or "", param3 or ""]) + "\n"

    # Call the shortcut via the macOS 'shortcuts' CLI
    try:
        proc = subprocess.run(
            ["shortcuts", "run", "switch"],
            input=payload.encode("utf-8"),
            capture_output=True,
            check=True
        )
        return proc.stdout.decode("utf-8").strip() or "OK"
    except subprocess.CalledProcessError as e:
        # Return stderr if the shortcut fails
        return f"Error: {e.stderr.decode('utf-8').strip()}"


if __name__ == "__main__":
    # Run over stdio transport by default
    mcp.run(transport="stdio")
