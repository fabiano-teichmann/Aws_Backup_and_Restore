import os
from unittest import TestCase

from backup_database import Backup


class TestBackup_database(TestCase):
    def setUp(self) -> None:
        self.backup = Backup()
        self.folder = self.backup.folder

    def test_dump_database(self):
        """Must be return True if success dump database"""
        self.assertEqual(self.backup.dump(), True)

    def test_zip_folder(self):
        """Must be return path file created"""
        self.assertEqual(os.path.isfile(self.backup.zip_folder()), True)

    def test_remove_dir(self):
        """Must be remove folder"""
        self.assertEqual(self.backup.remove_folder(), True)

    def test_upload_s3(self):
        """Must be return code 200"""
        self.assertEqual(self.backup.upload_s3(, 200))