import os
import unittest as ut
import shutil
from time import sleep

from models.files import Dir, File
from models.source import Source


TEST_DIR = 'tmp/test'


class TestBackup(ut.TestCase):
    def setUp(self):
        os.mkdir(TEST_DIR)

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def test_source_add(self):
        Dir(name='backups').generate_to(TEST_DIR)
        test_struct = self._init_test_struct()
        self._make_backup()
        backup_struct = self._create_backup_structure(index=0)
        backup_struct.name = 'test-dir'
        self.assertTrue(test_struct.equal(backup_struct, with_content=True))

    def test_file_add_root(self):
        Dir(name='backups').generate_to(TEST_DIR)
        test_struct = self._init_test_struct()
        self._make_backup()

        sleep(1.0)

        with open(os.path.join(TEST_DIR, 'test-dir/new.txt'), 'w') as f:
            f.write('1')
        test_struct.files.append(File(name='new.txt', content='1'))
        self._make_backup()

        backup_struct = self._create_backup_structure(index=1)
        backup_struct.name = 'test-dir'
        self.assertTrue(test_struct.equal(backup_struct, with_content=True))

        backup_struct = self._create_backup_structure(index=0)
        backup_struct.name = 'prev'
        prev_struct = Dir(name='prev', files=[File(name='.added.pybackup', content='./new.txt\n')])
        self.assertTrue(prev_struct.equal(backup_struct, with_content=True))

    def _init_test_struct(self):
        test_struct = Dir(
            name='test-dir',
            dirs=[
                Dir(
                    name='f1',
                    dirs=[
                        Dir(
                            name='f11',
                            dirs=[],
                            files=[
                                File(name='t11-1.txt'),
                                File(name='t11-2.txt'),
                            ]
                        )
                    ],
                    files=[
                        File(name='t1-1.txt'),
                    ]
                ),
                Dir(
                    name='f2',
                    dirs=[
                        Dir(
                            name='f22',
                            dirs=[],
                            files=[]
                        )
                    ],
                    files=[
                        File(name='t2-1.txt'),
                    ]
                ),
                Dir(
                    name='f3',
                    dirs=[],
                    files=[]
                )
            ],
            files=[
                File(name='1.txt'),
                File(name='2.txt'),
            ]
        )
        test_struct.generate_to(TEST_DIR)
        return test_struct

    def _make_backup(self):
        source_dir = os.path.join(TEST_DIR, 'test-dir')
        target_dir = os.path.join(TEST_DIR, 'backups')

        # Backup
        source = Source(source_dir, target_dir)
        source.backup()

    def _create_backup_structure(self, index):
        target_dir = os.path.join(TEST_DIR, 'backups')

        # Target home check
        self.assertEqual(len(os.listdir(target_dir)), 1)
        self.assertTrue(os.listdir(target_dir)[0].endswith('test-dir'))
        trg_home = os.path.join(target_dir, os.listdir(target_dir)[0])

        # Backup folder check
        backups = sorted(os.listdir(trg_home))
        backup_dir = os.path.join(trg_home, backups[index])

        # Creating backup structure
        backup_struct = Dir.create_from(backup_dir, with_content=True)

        return backup_struct
