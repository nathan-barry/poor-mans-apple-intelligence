import subprocess
from dataclasses import dataclass
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ShortcutRunner")


@dataclass
class Command:
    function: str
    arg_1: str = " "
    arg_2: str = " "
    arg_3: str = " "

    def payload(self) -> str:
        """
        Build the four-line payload for the shortcut:
          1) function name
          2) arg_1
          3) arg_2
          4) arg_3
        """
        return "\n".join([self.function, self.arg_1, self.arg_2, self.arg_3])


def run_command(cmd: Command) -> str:
    """
    Invoke the 'switch' Apple Shortcut with the given Command.payload(),
    returning stdout or stderr on failure.
    """
    try:
        proc = subprocess.run(
            ["shortcuts", "run", "switch"],
            input=cmd.payload().encode("utf-8"),
            capture_output=True,
            check=True,
        )
        out = proc.stdout.decode("utf-8").strip()
        return out or "OK"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.decode('utf-8').strip()}"


# —————— Tools ——————

@mcp.tool()
def sendMessage(name: str, message: str) -> str:
    return run_command(Command("sendMessage", name, message))


@mcp.tool()
def phoneCall(name: str) -> str:
    return run_command(Command("phoneCall", name))


@mcp.tool()
def facetimeCall(name: str) -> str:
    return run_command(Command("facetimeCall", name))


@mcp.tool()
def sendEmail(name: str, message: str, subject: str) -> str:
    return run_command(Command("sendEmail", name, message, subject))


@mcp.tool()
def listContacts() -> str:
    return run_command(Command("listContacts"))


@mcp.tool()
def listPastCalendarEvents(number: int, unit: str) -> str:
    return run_command(Command("listPastCalendarEvents", str(number), unit))


@mcp.tool()
def listFutureCalendarEvents(number: int, unit: str) -> str:
    return run_command(Command("listFutureCalendarEvents", str(number), unit))


@mcp.tool()
def listTodayCalendarEvents() -> str:
    return run_command(Command("listTodayCalendarEvents"))


@mcp.tool()
def createCalendarEvent(title: str, start_time: str, end_time: str) -> str:
    return run_command(Command("createCalendarEvent", title, start_time, end_time))


@mcp.tool()
def listReminders() -> str:
    return run_command(Command("listReminders"))


@mcp.tool()
def addReminder(reminder_name: str, list_name: str) -> str:
    return run_command(Command("addReminder", reminder_name, list_name))


@mcp.tool()
def getCurrentWeather() -> str:
    return run_command(Command("getCurrentWeather"))


@mcp.tool()
def getWeatherForecast() -> str:
    return run_command(Command("getWeatherForecast"))


@mcp.tool()
def setAlarm(alarm_name: str, time: str) -> str:
    return run_command(Command("setAlarm", alarm_name, time))


@mcp.tool()
def deleteAlarm(alarm_name: str) -> str:
    return run_command(Command("deleteAlarm", alarm_name))


@mcp.tool()
def listAlarms() -> str:
    return run_command(Command("listAlarms"))


if __name__ == "__main__":
    # By default this will use the stdio transport
    mcp.run(transport="stdio")
