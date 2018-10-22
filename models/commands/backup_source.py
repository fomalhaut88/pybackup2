from models.base_command import BaseCommand
from models.source import SourceList


class BackupSource(BaseCommand):
    title = 'backup-source'
    args = ('source_hash',)
    doc = "Backups the source."

    def execute(self):
        source_list = SourceList()
        source = source_list[self.args['source_hash']]
        updated = source.backup()
        if updated:
            print("backup completed")
        else:
            print("no changes")
