import sys

from models.commands import run_command
from models.terminal import Terminal


if __name__ == "__main__":
    argv = sys.argv[1:]

    if argv:
        name, *args = argv
        run_command(name, args)
    else:
        terminal = Terminal()
        terminal.run()
