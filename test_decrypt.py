from init import DBUtils, OSUtils, ProcessRequest
import os
import shutil

DB_FILE = "./test.db"
EXTENTION = 'l2.gpg'
IGNORE_FILE_TYPES = ['prop']
ALLOW_DUPLICATE_FILES = True
SRC_LOCATION ='./test/test_data/dest_location'
DEST_LOCATION = 'test/test_data/restore'

if __name__ == '__main__':
    
    # check the db, remove the restore data
    if not os.path.exists(DB_FILE):
        print('missing db index, exiting')
        exit()
        
    if os.path.exists(DEST_LOCATION):
        shutil.rmtree(DEST_LOCATION)
    
    osUtils = OSUtils(EXTENTION, IGNORE_FILE_TYPES)
    process_config = {
        "layer_1_passwd": "123",
        "layer_1_passwd": "321",
        "allow_duplicates": ALLOW_DUPLICATE_FILES,
    }
    process_user_request = ProcessRequest(
        DBUtils(DB_FILE), osUtils, process_config)
    response = process_user_request.start_decryption(
        SRC_LOCATION, DEST_LOCATION)

    # {'operation': 'dec', 'total_from_db': 20, 'ignored_count': 0, 'success_count': 20, 'failed_count': 0}
    if response['operation'] ==  'dec' and response['total_from_db'] ==  20 and response['failed_count'] ==  0:
        print("PASS")
    else:
        print(response)