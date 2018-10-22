import os
import json
import shutil
import traceback
from hashlib import md5
from datetime import datetime

from models import CONFIG_PATH, utils
from models.scanner import Scanner
from models.changes import AddedChange, RemovedChange, UpdatedChange


class Source:
    ADDED_FILE = '.added.pybackup'

    def __init__(self, src, trg):
        self.src = utils.clean_dir(src)
        self.trg = utils.clean_dir(trg)
        self.hash = self._calc_hash()
        self.trg_home = self._calc_trg_home()

    def backup(self):
        self._ensure_trg_home()
        backups = self.get_backups()

        updated = False

        if backups:
            backup_last_dir = os.path.join(self.trg_home, backups[-1])

            scanner = Scanner()
            changes = scanner.scan(self.src, backup_last_dir)

            if changes:
                backup_new = self._generate_new_backup()
                backup_new_dir = os.path.join(self.trg_home, backup_new)

                os.rename(backup_last_dir, backup_new_dir)
                os.mkdir(backup_last_dir)

                for change in changes:
                    try:
                        folder, basename = os.path.split(change.path)

                        if isinstance(change, AddedChange):
                            utils.ensure_dir(os.path.join(backup_new_dir, folder))
                            if os.path.isdir(os.path.join(self.src, change.path)):
                                shutil.copytree(
                                    os.path.join(self.src, change.path),
                                    os.path.join(backup_new_dir, change.path)
                                )
                            else:
                                shutil.copyfile(
                                    os.path.join(self.src, change.path),
                                    os.path.join(backup_new_dir, change.path)
                                )

                            added_path = os.path.join(backup_last_dir, self.ADDED_FILE)
                            with open(added_path, 'a') as f:
                                print(change.path, file=f)

                        elif isinstance(change, RemovedChange):
                            utils.ensure_dir(os.path.join(backup_last_dir, folder))
                            os.rename(
                                os.path.join(backup_new_dir, change.path),
                                os.path.join(backup_last_dir, change.path)
                            )

                        elif isinstance(change, UpdatedChange):
                            utils.ensure_dir(os.path.join(backup_last_dir, folder))
                            os.rename(
                                os.path.join(backup_new_dir, change.path),
                                os.path.join(backup_last_dir, change.path)
                            )
                            shutil.copyfile(
                                os.path.join(self.src, change.path),
                                os.path.join(backup_new_dir, change.path)
                            )

                        updated = True

                    except:
                        print("Error in {}".format(change))
                        traceback.print_exc()

            if not updated:
                if not os.listdir(backup_last_dir):
                    os.rmdir(backup_last_dir)

        else:
            backup_new = self._generate_new_backup()
            backup_new_dir = os.path.join(self.trg_home, backup_new)
            shutil.copytree(self.src, backup_new_dir)
            updated = True

        return updated

    def remove_trg(self):
        shutil.rmtree(self.trg_home)

    def get_backups(self):
        return sorted(os.listdir(self.trg_home))

    def get_file_changes(self, rel_path):
        for backup in self.get_backups():
            backup_dir = os.path.join(self.trg_home, backup)
            path = os.path.join(backup_dir, rel_path)
            if os.path.exists(path):
                yield backup

    def get_file_content(self, rel_path, backup):
        backup_dir = os.path.join(self.trg_home, backup)
        path = os.path.join(backup_dir, rel_path)
        with open(path) as f:
            return f.read()

    def restore_file(self, rel_path, backup):
        backup_dir = os.path.join(self.trg_home, backup)
        t_path = os.path.join(backup_dir, rel_path)
        s_path = os.path.join(self.src, rel_path)
        shutil.copyfile(t_path, s_path)

    def _calc_hash(self):
        m = md5()
        m.update(self.src.encode())
        m.update(self.trg.encode())
        return m.hexdigest()

    def _calc_trg_home(self):
        trg_home = self.src
        trg_home = trg_home.replace("/", "_")
        trg_home = trg_home.replace(":", "__")
        trg_home = os.path.join(self.trg, trg_home)
        return trg_home

    def _ensure_trg_home(self):
        if not os.path.exists(self.trg_home):
            os.mkdir(self.trg_home)

    @classmethod
    def _generate_new_backup(cls):
        return datetime.now().strftime("%Y%m%d%H%M%S")


class SourceList:
    path = os.path.join(CONFIG_PATH, 'targets.json')

    def __init__(self):
        self._dct = {}
        self._load_dct()

    def __bool__(self):
        return bool(self._dct)

    def __getitem__(self, hash_):
        return self._dct.get(hash_)

    def __iter__(self):
        yield from self._dct.values()

    def __contains__(self, source):
        return source.hash in self._dct

    def add(self, source):
        self._dct[source.hash] = source

    def remove(self, source):
        del self._dct[source.hash]

    def update(self):
        data = []
        for source in self._dct.values():
            data.append({'src': source.src, 'trg': source.trg})
        with open(self.path, 'w') as f:
            json.dump(data, f)

    def _load_dct(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                for item in json.load(f):
                    source = Source(item['src'], item['trg'])
                    self._dct[source.hash] = source
