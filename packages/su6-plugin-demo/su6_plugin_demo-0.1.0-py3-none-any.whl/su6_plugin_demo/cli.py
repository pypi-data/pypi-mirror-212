"""
This module contains an example of both methods of adding commands to su6.
"""

from su6.plugins import register, run_tool

# or: from su6 import register_plugin, run_tool
from typer import Typer

# method 1: adding top-level commands


@register
def first() -> int:
    """
    Register a top-level command.

    @register works without ()
    """
    print("This is a demo command!")
    return 0


@register()
def second() -> int:
    """
    Register a top-level command.

    @register also works with ()
    """
    print("This is another demo command (with exit code)!")
    run_tool("echo", "args", "go", "here")
    return 1


@register(name="third")
def yet_another() -> bool:
    """
    Register a top-level command.

    @register works with extra Typer arguments.
    """
    print("This is another demo command (with bool exit)!")
    return True


# method 2: adding a namespace (based on the plugin package name)

app = Typer()


@app.command()
def subcommand() -> None:
    """
    Register a plugin-level command.

    Can be used as `su6 demo subcommand` (in this case, the plugin name is demo)
    """
    print("this lives in a namespace")
