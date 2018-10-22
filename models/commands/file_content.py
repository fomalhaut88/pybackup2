from models.base_command import BaseCommand
from models.source import SourceList


class FileContent(BaseCommand):
    title = 'file-content'
    args = ('source_hash', 'file_path', 'backup')
    doc = "Outputs the content of the file from the specified backup."

    def execute(self):
        source_list = SourceList()
        source = source_list[self.args['source_hash']]
        content = source.get_file_content(self.args['file_path'], self.args['backup'])
        print(content)
