from typing import TYPE_CHECKING, Any

from cleo.application import Application

import commands

if TYPE_CHECKING:
    from starlite import Starlite


class Cli:
    def __init__(self, starletapp: Starlite):
        self.st_app = starletapp
        self.cli = Application()
        for command in commands.__all__:
            cli_command = getattr(commands, command)
            try:
                self.cli.add(cli_command())
            except Exception:
                self.cli.add(cli_command(self.st_app))

    def run(self) -> int | Any:
        """start Cleo."""
        return self.cli.run()
