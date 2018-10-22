import traceback

from models.base_command import BaseCommand
from models.source import SourceList


class BackupAll(BaseCommand):
    title = 'backup-all'
    args = ()
    doc = "Backups all the sources."

    def execute(self):
        source_list = SourceList()
        for source in source_list:
            try:
                print("backuping {} -> {} ...".format(source.src, source.trg))
                updated = source.backup()
                if updated:
                    print("backup completed")
                else:
                    print("no changes")
            except:
                traceback.print_exc()
