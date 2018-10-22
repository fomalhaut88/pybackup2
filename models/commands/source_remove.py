from models.base_command import BaseCommand
from models.source import SourceList
from models.errors import CommandError


class SourceRemove(BaseCommand):
    title = 'source-remove'
    args = ('source_hash',)
    doc = "Removes the source."

    def execute(self):
        source_list = SourceList()
        source = source_list[self.args['source_hash']]

        if source is not None:
            source.remove_trg()

            source_list.remove(source)
            source_list.update()

            print("source has been removed successfully")

        else:
            raise CommandError("no such source")
