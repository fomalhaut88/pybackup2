from time import sleep

from models.base_command import BaseCommand
from models.source import SourceList


class Daemon(BaseCommand):
    title = 'daemon'
    args = ('timeout',)
    doc = "Backups all the sources periodically with timeout."

    def execute(self):
        timeout = int(self.args['timeout'])
        while True:
            source_list = SourceList()
            for source in source_list:
                try:
                    source.backup()
                except:
                    pass
            sleep(timeout)
