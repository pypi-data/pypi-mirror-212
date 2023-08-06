from su6 import app
from typer.testing import CliRunner

from src.su6_plugin_demo.cli import first, second, subcommand, yet_another

runner = CliRunner(mix_stderr=False)


def test_runner_call():
    result = runner.invoke(app, ["first"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["second"])
    assert result.exit_code == 1

    result = runner.invoke(app, ["third"])
    assert result.exit_code == 1

    result = runner.invoke(app, ["fourth"])
    assert result.exit_code > 0

    result = runner.invoke(app, ["demo", "subcommand"])
    assert result.exit_code == 0


def test_direct_call():
    assert not first()
    assert second()
    assert yet_another()
    assert not subcommand()
