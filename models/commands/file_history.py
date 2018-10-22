from models.base_command import BaseCommand
from models.source import SourceList


class FileHistory(BaseCommand):
    title = 'file-history'
    args = ('source_hash', 'file_path')
    doc = "Outputs all states of the file in backups."

    def execute(self):
        source_list = SourceList()
        source = source_list[self.args['source_hash']]
        for backup in source.get_file_changes(self.args['file_path']):
            print(backup)
