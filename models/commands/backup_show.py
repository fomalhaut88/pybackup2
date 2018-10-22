from models.base_command import BaseCommand
from models.source import SourceList


class BackupShow(BaseCommand):
    title = 'backup-show'
    args = ('source_hash',)
    doc = "Outputs backups of the specified source."

    def execute(self):
        source_list = SourceList()
        source = source_list[self.args['source_hash']]
        if source is not None:
            for backup in source.get_backups():
                print(backup)
        else:
            print("no such source")
