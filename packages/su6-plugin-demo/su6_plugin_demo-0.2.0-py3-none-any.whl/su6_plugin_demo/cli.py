"""
This module contains an example of both methods of adding commands to su6.
"""
import typing

from su6.plugins import PluginConfig, print, register, run_tool

# or: from su6 import register_plugin, run_tool
from typer import Typer

# method 1: adding top-level commands


@register(with_state=True, config_key="demo.extra")
class MoreDemoConfig(PluginConfig):
    """
    Config that loads 'state' into self.state and loads [tool.su6.demo.extra] from pyproject.toml into self.
    """

    more: bool


@register
class DemoConfig(PluginConfig):
    """
    Config without state, loads [tool.su6.demo] from pyproject.toml into self.
    """

    required_arg: str
    boolean_arg: bool
    optional_with_default: typing.Optional[str] = None
    more: PluginConfig = MoreDemoConfig(more=False)


config = DemoConfig()


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


@register()
def with_arguments(required_arg: str, boolean_arg: bool = False) -> None:
    """
    Register a top-level command.

    @register works with extra Typer arguments.
    """
    config.update(required_arg=required_arg, boolean_arg=boolean_arg)
    print(config)
    assert (
        config.more.state
        and config.more.state.config
        and config.more.extras["state"].config
        and config.more.extras["state"]
        and config.more.state.config.pyproject == config.more.extras["state"].config.pyproject
    )


# method 2: adding a namespace (based on the plugin package name)

app = Typer()


@app.command()
def subcommand() -> None:
    """
    Register a plugin-level command.

    Can be used as `su6 demo subcommand` (in this case, the plugin name is demo)
    """
    print("this lives in a namespace")
