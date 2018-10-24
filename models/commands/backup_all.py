import traceback

from models.base_command import BaseCommand
from models.source import SourceList


class BackupAll(BaseCommand):
    title = 'backup-all'
    args = ()
    doc = "Backups all the sources."

    def execute(self):
        source_list = SourceList()
        if source_list:
            for source in source_list:
                try:
                    print("backup {} -> {} ...".format(source.src, source.trg))
                    updated = source.backup()
                    if updated:
                        print("backup completed")
                    else:
                        print("no changes")
                except:
                    traceback.print_exc()
        else:
            print("no sources to backup")
