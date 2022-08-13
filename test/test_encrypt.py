from init import DBUtils, OSUtils, ProcessRequest
import os
import sys
import shutil
import unittest
sys.path.append(os.path.abspath(os.path.join('..')))


class EncryptTestCase(unittest.TestCase):

    def setUp(self):
        self.DB_FILE = "test.db"
        self.EXTENTION = 'l2.gpg'
        self.IGNORE_FILE_TYPES = ['prop']
        self.ALLOW_DUPLICATE_FILES = True
        self.DEST_LOCATION = './test_data/dest_location'
        self.SRC_LOCATION = './test_data/source_location'

    def tearDown(self):
        print('clean the db, remove the enc. files')
        if os.path.exists(self.DB_FILE):
            os.remove(self.DB_FILE)

    """ test the full encryption process """

    def test_encryption_process(self):
        osUtils = OSUtils(self.EXTENTION, self.IGNORE_FILE_TYPES)
        process_config = {
            "layer_1_passwd": "123",
            "layer_2_passwd": "321",
            "allow_duplicates": self.ALLOW_DUPLICATE_FILES,
        }
        process_user_request = ProcessRequest(
            DBUtils(self.DB_FILE), osUtils, process_config)
        response = process_user_request.start_encryption(
            self.SRC_LOCATION, self.DEST_LOCATION)

        # {'operation': 'enc', 'total_count': 21, 'duplicate_count': 1, 'success_count': 20, 'failed_count': 1}
        self.assertTrue(response['operation'] == 'enc' and response['total_count']
                        == 21 and response['success_count'] == 20, 'encryption process failed')
