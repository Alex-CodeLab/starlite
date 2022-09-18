from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.io.inputs import option

from starlite import Starlite


class ListRoutes(Command):  # type: ignore
    name: str = "routes"
    description: str = "show all available routes"
    arguments: list[argument] = []
    options: list[option] = []

    def __init__(self, app: Starlite) -> None:
        self.app = app
        super().__init__()

    def handle(self) -> None:
        """print routes."""
        for route in self.app.routes:
            self.line(
                f"<comment>{route.path:<25}</comment> {route.handler_names[0] if len(route.handler_names) > 0 else route.handler_names:<25}"
                + str(route.methods)
            )
