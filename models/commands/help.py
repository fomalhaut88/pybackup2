import os

from models.base_command import BaseCommand
from models.commands import _commands_map


class Help(BaseCommand):
    title = 'help'
    args = ()
    doc = "Prints help for each command."

    def execute(self):
        print("Help:")
        for klass in _commands_map.values():
            self._print_class_help(klass)
        self._print_exit_help()

    def _print_class_help(self, klass):
        args_str = " ".join("[{}]".format(arg.upper()) for arg in klass.args)
        print("    {} {}".format(klass.title, args_str))
        print("       - {}".format(klass.doc))
        print()

    def _print_exit_help(self):
        print("    exit")
        print("       - Leaves Pybackup.")
        print()
