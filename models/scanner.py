import os
import filecmp

from models.changes import AddedChange, RemovedChange, UpdatedChange


class Scanner:
    def __init__(self):
        pass

    def scan(self, folder1, folder2):
        changes = []

        dct1 = self._collect_files(folder1)
        dct2 = self._collect_files(folder2)

        keys_common = dct1.keys() & dct2.keys()
        keys_to_add = dct1.keys() - dct2.keys()
        keys_to_remove = dct2.keys() - dct1.keys()

        for rel_path in keys_to_remove:
            changes.append(RemovedChange(rel_path))

        for rel_path in keys_to_add:
            changes.append(AddedChange(rel_path))

        for rel_path in keys_common:
            dirnames1 = dct1[rel_path]['dirnames']
            dirnames2 = dct2[rel_path]['dirnames']

            dirnames_common = dirnames1 & dirnames2
            dirnames_to_add = dirnames1 - dirnames2
            dirnames_to_remove = dirnames2 - dirnames1

            for dirname in dirnames_to_remove:
                filepath = os.path.join(rel_path, dirname)
                changes.append(RemovedChange(filepath))

            for dirname in dirnames_to_add:
                filepath = os.path.join(rel_path, dirname)
                changes.append(AddedChange(filepath))

            for dirname in dirnames_common:
                filepath = os.path.join(rel_path, dirname)
                path1 = os.path.join(folder1, filepath)
                path2 = os.path.join(folder2, filepath)

                if not self._files_equal(path1, path2):
                    changes.append(UpdatedChange(filepath))

        for rel_path in keys_common:
            filenames1 = dct1[rel_path]['filenames']
            filenames2 = dct2[rel_path]['filenames']

            filenames_common = filenames1 & filenames2
            filenames_to_add = filenames1 - filenames2
            filenames_to_remove = filenames2 - filenames1

            for filename in filenames_to_remove:
                filepath = os.path.join(rel_path, filename)
                changes.append(RemovedChange(filepath))

            for filename in filenames_to_add:
                filepath = os.path.join(rel_path, filename)
                changes.append(AddedChange(filepath))

            for filename in filenames_common:
                filepath = os.path.join(rel_path, filename)
                path1 = os.path.join(folder1, filepath)
                path2 = os.path.join(folder2, filepath)

                if not self._files_equal(path1, path2):
                    changes.append(UpdatedChange(filepath))

        self._reduce_changes(changes)

        return changes

    def _collect_files(self, folder):
        dct = {}
        for root_path, folders, filenames in os.walk(folder):
            rel_path = os.path.relpath(root_path, folder)
            dct[rel_path] = {
                'dirnames': set(folders),
                'filenames': set(filenames)
            }
        return dct

    def _reduce_changes(self, changes):
        changes.sort(key=lambda change: change.path)

        added = []
        removed = []
        indices = []
        for i, change in enumerate(changes):
            if isinstance(change, AddedChange):
                found = False
                for path in added:
                    if change.path.startswith(path):
                        indices.append(i)
                        found = True
                        break
                if not found:
                    added.append(change.path)

            if isinstance(change, RemovedChange):
                found = False
                for path in removed:
                    if change.path.startswith(path):
                        indices.append(i)
                        found = True
                        break
                if not found:
                    removed.append(change.path)

        for i in sorted(indices, reverse=True):
            del changes[i]

    @classmethod
    def _files_equal(cls, path1, path2):
        if os.path.isfile(path1) and os.path.isfile(path2):
            return filecmp.cmp(path1, path2)
        else:
            return os.path.isfile(path1) == os.path.isfile(path2)
