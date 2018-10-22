import os
import shutil
from datetime import datetime


class Backuper:
    def __init__(self, source):
        self.source = source

    @classmethod
    def generate_new(cls):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def src_stringified(self):
        s = self.source.src
        s = s.replace(os.sep, '_')
        s = s.replace(':', '__')
        return s

    def get_folder(self):
        return os.path.join(
            self.source.trg,
            self.src_stringified()
        )

    def is_initialized(self):
        folder = self.get_folder()
        return os.path.exists(folder) and self.get_backups()

    def initialize(self):
        folder = self.get_folder()
        if not os.path.exists(folder):
            os.mkdir(folder)
        new = self.generate_new()
        trg_path = os.path.join(folder, new)
        shutil.copytree(self.source.src, trg_path)

    def get_backups(self):
        folder = self.get_folder()
        return sorted(os.listdir(folder))

    def get_last_backup_path(self):
        folder = self.get_folder()
        last_backup = sorted(os.listdir(folder))[-1]
        path = os.path.join(folder, last_backup)
        return path

    def backup(self, changes):
        folder = self.get_folder()
        backups = sorted(os.listdir(folder))
        old = backups[-1]
        new = self.generate_new()

        old_path = os.path.join(folder, old)
        new_path = os.path.join(folder, new)

        print(old, new)
        print(changes)
