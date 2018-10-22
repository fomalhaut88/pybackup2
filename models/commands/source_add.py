import os

from models.base_command import BaseCommand
from models.source import Source, SourceList
from models.errors import CommandError


class SourceAdd(BaseCommand):
    title = 'source-add'
    args = ('source_dir', 'target_dir')
    doc = "Adds the source."

    def execute(self):
        source = Source(self.args['source_dir'], self.args['target_dir'])

        source_list = SourceList()

        if source in source_list:
            raise CommandError("such source already exists")

        source.backup()

        source_list.add(source)
        source_list.update()

        print("the source has been added successfully")
