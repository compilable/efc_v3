
import sqlite3
from sqlite3 import Error, IntegrityError
import hashlib
import os
import subprocess
from os.path import exists


DB_FILE="./data.db"
EXTENTION='l2.gpg'

def encrypt_file(source_file,destination_folder,passwd):
    file_name = os.path.basename(source_file) + '.' + EXTENTION
    destination = os.path.join(destination_folder, file_name)
    subprocess.run(["gpg", "-o", destination, "--symmetric", "--cipher-algo",  "AES256",  "--batch", "--yes",  "--passphrase", passwd, source_file])
    if exists(destination):
        return generate_hash(destination)

def create_record(file):
    file_name = os.path.basename(file)
    file_record= (file_name, generate_hash(file))
    
    try:
        conn = sqlite3.connect(DB_FILE)

        if conn is not None:
            sql = ''' INSERT INTO FILE_INDEX(name,hash) VALUES(?,?) '''
            cur = conn.cursor()
            cur.execute(sql, file_record)
            conn.commit()
            print(cur.lastrowid)
        else:
            print("Error! when inserting to the table.")

    except IntegrityError as e: 
        print('File ` %s ` exists with the same name and hash.' %(file_name))
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()           

def generate_hash(file):
    BLOCK_SIZE = 65536 # The size of each read from the file

    file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file

    #print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash 
    return file_hash.hexdigest()

def create_db():
    """ create a database connection to a SQLite database """
    conn = None

    index_table_sql = """ CREATE TABLE IF NOT EXISTS FILE_INDEX (
                                           file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name text NOT NULL,
                                            hash text,
                                            ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                                            UNIQUE(name,hash)
                                        ); """
    try:
        conn = sqlite3.connect(DB_FILE)
        print(sqlite3.version)

        # create tables
        if conn is not None:
            # create projects table
            cursor = conn.cursor()
            cursor.execute(index_table_sql)
        else:
            print("Error! when creating the table.")

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    print('refer to stage 1 features')

