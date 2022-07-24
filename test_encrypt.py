
from init import DBUtils, OSUtils, ProcessRequest
import os
import shutil

DB_FILE = "./test.db"
EXTENTION = 'l2.gpg'
IGNORE_FILE_TYPES = ['prop']
ALLOW_DUPLICATE_FILES = True
DEST_LOCATION ='./test/test_data/dest_location'   
SRC_LOCATION='./test/test_data/source_location'

def clean_data():
    # clean the db, remove the enc. files
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    if os.path.exists(DEST_LOCATION):
        shutil.rmtree(DEST_LOCATION)
        
        
if __name__ == '__main__':
    
    clean_data()
    
    osUtils = OSUtils(EXTENTION, IGNORE_FILE_TYPES)
    process_config = {
        "layer_1_passwd": "123",
        "layer_2_passwd": "321",
        "allow_duplicates": ALLOW_DUPLICATE_FILES,
    }
    process_user_request = ProcessRequest(
        DBUtils(DB_FILE), osUtils, process_config)
    response = process_user_request.start_encryption(
        SRC_LOCATION,DEST_LOCATION )
    
    # {'operation': 'enc', 'total_count': 21, 'duplicate_count': 1, 'success_count': 20, 'failed_count': 1}
    if response['operation'] ==  'enc' and response['total_count'] ==  21 and response['success_count'] ==  20:
        print("PASS")
        # clean_data()
    else:
        print(response)