from inspect import getfullargspec
from typing import TYPE_CHECKING
from importlib import import_module
from cleo import Application, Command
from typing import Callable


if TYPE_CHECKING:
    from starlite.app import Starlite

class CLI:
    """Add CLI commands using cleo https://github.com/python-poetry/cleo.

    usage example:

    # ...
    app = Starlite(route_handlers=[])
    if __name__ == '__main__':
        from commands.cli import CLI
        cli = Cli(app)
        cli.register(ListRoutes)
        cli.register(StartProject)
        cli.run()
    """

    def __init__(self, app: "Starlite"):
        self.st_app = app
        self.cli_ = Application()
        self.commands: list[Callable[..., Command]] = []

    def register(self, command: Callable[..., Command]) -> None:
        self.commands.append(command)

    def run(self) -> int:
        """start Cleo."""
        for command in self.commands:
            import_module(f"commands.{command.name}")
            arg_spec = getfullargspec(command)
            if "app" in arg_spec.args:
                self.cli_.add(command(self.st_app))
            else:
                self.cli_.add(command())  # pylint: disable = no-value-for-parameter

        errorcode: int = self.cli_.run()
        return errorcode
