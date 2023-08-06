import typer
from enum import Enum


class TyperExt:
    def __init__(self) -> None:
        pass

    class Colors(Enum):
        BLACK = "black"
        RED = "red"
        GREEN = "green"
        YELLOW = "yellow"
        BLUE = "blue"
        MAGENTA = "magenta"
        CYAN = "cyan"
        WHITE = "white"
        RESET = "reset"
        BRIGHT_BLACK = "bright_black"
        BRIGHT_RED = "bright_red"
        BRIGHT_GREEN = "bright_green"
        BRIGHT_YELLOW = "bright_yellow"
        BRIGHT_BLUE = "bright_blue"
        BRIGHT_MAGENTA = "bright_magenta"
        BRIGHT_CYAN = "bright_cyan"
        BRIGHT_WHITE = "bright_white"

    def check_colors_exists(self, query: str):
        return True if any(x for x in self.Colors if x.name == query) else False

    def raise_error(self, error, msg: str):
        typer.secho(f'{msg}', fg=typer.colors.RED)
        raise typer.Exit(error)

    def attach_log(self, msg: str, color: Colors):
        if self.check_colors_exists(color.name):
            typer.secho(f'{msg}', fg=color.value)
        else:
            self.raise_error("UnSupport Color Type")

    # def attach_log(self, tag, msg, color):
    #     if self.check_colors_exists(color.name):
    #         typer.secho(f'[{tag}]: {msg}', fg=color)
    #     else:
    #         self.raise_error("UnSupport Color Type")
