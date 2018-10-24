import os
import inspect
import traceback

from models.base_command import BaseCommand
from models.errors import CommandError


_commands_map = {}


def run_command(name, args):
    if not _commands_map:
        _build_commands_map()

    try:
        if name not in _commands_map:
            raise CommandError("no such command")

        klass = _commands_map[name]
        command = klass(*args)
        command.execute()

    except CommandError as err:
        print("Error: {}".format(err))

    except:
        traceback.print_exc()


def _build_commands_map():
    from models.commands import (
        version, help,
        source_show, source_add, source_remove,
        backup_source, backup_all, backup_show,
        file_history, file_content, file_restore,
        daemon
    )

    klasses = [
        version.Version,
        help.Help,
        source_show.SourceShow,
        source_add.SourceAdd,
        source_remove.SourceRemove,
        backup_source.BackupSource,
        backup_all.BackupAll,
        backup_show.BackupShow,
        file_history.FileHistory,
        file_content.FileContent,
        file_restore.FileRestore,
        daemon.Daemon
    ]

    _commands_map.clear()
    for klass in klasses:
        _commands_map[klass.title] = klass
