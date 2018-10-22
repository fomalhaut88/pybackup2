from models.base_command import BaseCommand
from models.source import SourceList


class FileRestore(BaseCommand):
    title = 'file-restore'
    args = ('source_hash', 'file_path', 'backup')
    doc = "Restores the file from the specified backup."

    def execute(self):
        source_list = SourceList()
        source = source_list[self.args['source_hash']]
        content = source.restore_file(self.args['file_path'], self.args['backup'])
        print('the file has been restored successfully')
