
from init import DBUtils, OSUtils, ProcessRequest

DB_FILE = "./test.db"
EXTENTION = 'l2.gpg'
IGNORE_FILE_TYPES = ['prop']
ALLOW_DUPLICATE_FILES = True

if __name__ == '__main__':
    osUtils = OSUtils(EXTENTION, IGNORE_FILE_TYPES)
    process_config = {
        "layer_1_passwd": "123",
        "layer_1_passwd": "321",
        "allow_duplicates": ALLOW_DUPLICATE_FILES,
    }
    process_user_request = ProcessRequest(
        DBUtils(DB_FILE), osUtils, process_config)
    process_user_request.start_decryption(
        'test/test_data/dest_location', 'test/test_data/restore')
