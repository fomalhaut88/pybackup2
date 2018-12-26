import os
import traceback
from datetime import datetime
from time import sleep

from models import CONFIG_PATH
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
                    error_log_path = os.path.join(CONFIG_PATH, 'error.log')
                    with open(error_log_path, 'a') as f:
                        print('[{}] {}'.format(datetime.now(), traceback.format_exc()), file=f)
                        f.flush()
                else:
                    backup_log_path = os.path.join(CONFIG_PATH, 'backup.log')
                    with open(backup_log_path, 'a') as f:
                        print('[{}] {} ({} -> {})'.format(datetime.now(), source.hash, source.src, source.trg), file=f)
                        f.flush()
            sleep(timeout)
