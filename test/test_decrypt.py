from init import DBUtils, OSUtils, ProcessRequest
import os
import sys
import shutil
import unittest
sys.path.append(os.path.abspath(os.path.join('..')))


class EncryptTestCase(unittest.TestCase):

    def setUp(self):
        self.DB_FILE = "test.db.l2.gpg"
        self.EXTENTION = 'l2.gpg'
        self.IGNORE_FILE_TYPES = ['prop']
        self.ALLOW_DUPLICATE_FILES = True
        self.SRC_LOCATION = './test_data/dest_location'
        self.DEST_LOCATION = './test_data/restore'
        self.DELETE_INDEX_AFTER = True

    def tearDown(self):
        print('check the db, remove the restore data')
        if os.path.exists(self.DEST_LOCATION):
            shutil.rmtree(self.DEST_LOCATION)
        if os.path.exists(self.SRC_LOCATION):
            shutil.rmtree(self.SRC_LOCATION)
        if os.path.exists(self.DB_FILE):
            os.remove(self.DB_FILE)

    """ test the full decryption process """

    def test_decryption_process(self):
        if not os.path.exists(self.DB_FILE):
            print('missing db index, exiting')
            exit()

        osUtils = OSUtils(self.EXTENTION, self.IGNORE_FILE_TYPES)
        process_config = {
            "layer_1_passwd": "123",
            "layer_2_passwd": "321",
            "allow_duplicates": self.ALLOW_DUPLICATE_FILES,
            "delete_index": self.DELETE_INDEX_AFTER
        }
        process_user_request = ProcessRequest(
            DBUtils(self.DB_FILE), osUtils, process_config)
        response = process_user_request.start_decryption(
            self.SRC_LOCATION, self.DEST_LOCATION)

        # {'operation': 'dec', 'total_from_db': 20, 'ignored_count': 0, 'success_count': 20, 'failed_count': 0}
        self.assertTrue(response['operation'] == 'dec' and response['total_from_db']
                        == 20 and response['failed_count'] == 0, 'decryption process failed!')
