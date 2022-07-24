import datetime
import socket
import sqlite3
import collections
from sqlite3 import Error, IntegrityError
import hashlib
import math
import os
import subprocess
from os.path import exists
from pathlib import Path
from unittest.mock import patch


class OSUtils:

    def __init__(self, enc_file_ext, ignore_file_list):
        self.ENC_FILE_EXTENTION = enc_file_ext
        self.IGNORE_FILE_LIST = ignore_file_list

    def file_size_to_text(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def encrypt_file(self, source_file, destination_folder, passwd):
        file_name = os.path.basename(
            source_file) + '.' + self.ENC_FILE_EXTENTION
        destination = os.path.join(destination_folder, file_name)
        subprocess.run(["gpg", "-o", destination, "--symmetric", "--cipher-algo",
                       "AES256",  "--batch", "--yes",  "--passphrase", passwd, source_file])
        if exists(destination):
            return [self.generate_hash(destination), os.path.basename(destination)]

    def decrypt_file(self, source_file, destination_folder, passwd):
        destination = os.path.join(os.path.dirname(os.path.abspath(
            destination_folder)), os.path.basename(destination_folder))

        if os.path.exists(source_file):
            Path(os.path.dirname(os.path.abspath(destination_folder))).mkdir(
                parents=True, exist_ok=True)
            subprocess.run(["gpg",  "--batch",  "--passphrase", passwd,
                           "--output", destination, "--decrypt", source_file])

        if exists(destination):
            return self.generate_hash(destination)

    def generate_hash(self, file):
        BLOCK_SIZE = 65536  # The size of each read from the file

        # Create the hash object, can use something other than `.sha256()` if you wish
        file_hash = hashlib.sha256()
        with open(file, 'rb') as f:  # Open the file to read it's bytes
            # Read from the file. Take in the amount declared above
            fb = f.read(BLOCK_SIZE)
            while len(fb) > 0:  # While there is still data being read from the file
                file_hash.update(fb)  # Update the hash
                fb = f.read(BLOCK_SIZE)  # Read the next block from the file

        # print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash
        return file_hash.hexdigest()

    # list files in dir, reccurasivly
    def list_files(self, source_folder, db_location):

        file_map = {}
        for dp, dn, files in os.walk(source_folder):
            # print(dp),
            for file in files:
                if Path(file).name != Path(db_location).name and str(Path(file).suffix).replace('.', '') not in self.IGNORE_FILE_LIST:
                    # print(Path(file).suffix)
                    file_name = os.path.join(dp, file)
                    file_map[os.path.basename(file_name)] = file_name

        # for f in file_list:
            # print(f)

        return collections.OrderedDict(sorted(file_map.items()))


class DBUtils:

    def __init__(self, db_file):
        self.DB_FILE = db_file

    def create_record(self, file_record, db_location=None):
        # (file_name, fq_file_path, file_hash,file_size, file_size_txt,file_exists)
        try:
            conn = sqlite3.connect(
                self.DB_FILE if db_location == None else db_location)

            if conn is not None:
                create_sql = ''' INSERT INTO FILE_INDEX(name,fq_path, ori_hash,size,size_text) VALUES(?,?,?,?,?) '''
                update_sql = """ UPDATE FILE_INDEX set name=? ,fq_path= ?, size =? ,size_text =?, last_update_ts=? WHERE  ori_hash =? """

                if file_record[5]:
                    print("update record")
                    cur = conn.cursor()
                    now = datetime.datetime.now()
                    text = os.getlogin()+'@'+socket.gethostname() + ' ' + str(now)
                    cur.execute(
                        update_sql, (file_record[0], file_record[1], file_record[3], file_record[4], text, file_record[2],))
                    conn.commit()
                    return cur.rowcount > 0
                else:
                    print("inserting record")
                    cur = conn.cursor()
                    cur.execute(
                        create_sql, (file_record[0], file_record[1], file_record[2], file_record[3], file_record[4],))
                    conn.commit()
                    return cur.rowcount > 0
            else:
                print("Error! when inserting/updating to the table.")
                return False

        except Error as e:
            print(e)
            return False
        finally:
            if conn:
                conn.close()

    def create_db(self, db_location=None):
        """ create a database connection to a SQLite database """
        conn = None

        table_sql = """ CREATE TABLE IF NOT EXISTS FILE_INDEX (
                                            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                name text NOT NULL,
                                                fq_path text NOT NULL,
                                                ori_hash text,
                                                enc_name text,
                                                enc_hash text,
                                                size number DEFAULT 0,
                                                size_text text,
                                                last_update_ts text,
                                                ts DATETIME DEFAULT CURRENT_TIMESTAMP); """
        index_sql = """ CREATE INDEX IF NOT EXISTS HASH_INDEX ON FILE_INDEX (ori_hash); """
        try:
            conn = sqlite3.connect(
                self.DB_FILE if db_location == None else db_location)
            print(sqlite3.version)

            # create tables
            if conn is not None:
                # create projects table
                cursor = conn.cursor()
                cursor.execute(table_sql)
                cursor.execute(index_sql)
            else:
                print("Error! when creating the table.")

        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    # select all new files from db
    def list_new_files_from_db(self, db_location=None):
        try:
            conn = sqlite3.connect(
                self.DB_FILE if db_location == None else db_location)

            if conn is not None:
                sql = ''' SELECT file_id,name,fq_path,ori_hash,size FROM FILE_INDEX WHERE enc_hash is NULL '''
                cur = conn.cursor()
                cur.execute(sql)
                file_list = cur.fetchall()
                # print(file_list)
                return file_list
            else:
                print("Error! when listing new files from table.")
                return []
        except Error as e:
            print(e)
            return []
        finally:
            if conn:
                conn.close()

    # select all enc, files from db
    def list_enc_files_from_db(self, db_location=None):
        try:
            conn = sqlite3.connect(
                self.DB_FILE if db_location == None else db_location)

            if conn is not None:
                sql = ''' SELECT file_id,name,fq_path,ori_hash,size,enc_name,enc_hash FROM FILE_INDEX WHERE enc_hash is NOT NULL '''
                cur = conn.cursor()
                cur.execute(sql)
                file_list = cur.fetchall()
                # print(file_list)
                return file_list
            else:
                print("Error! when listing enc. files.")
                return []
        except Error as e:
            print(e)
            return []
        finally:
            if conn:
                conn.close()

    def update_enc_file_data(self, file_id, enc_hash, enc_name, db_location=None):
        file_record = (enc_hash, enc_name, file_id)

        try:
            conn = sqlite3.connect(
                self.DB_FILE if db_location == None else db_location)

            if conn is not None:
                sql = ''' UPDATE FILE_INDEX SET enc_hash = ? , enc_name = ? WHERE  file_id = ? '''
                cur = conn.cursor()
                cur.execute(sql, file_record)
                conn.commit()
                return cur.rowcount > 0
            else:
                print("Error! when updating to the table.")
                return False
        except Error as e:
            print(e)
            return False
        finally:
            if conn:
                conn.close()

    # check file exists from enc_hash
    def find_existing_file_from_hash(self, file_hash, db_location=None):
        try:
            conn = sqlite3.connect(
                self.DB_FILE if db_location == None else db_location)

            if conn is not None:
                sql = """ SELECT EXISTS (SELECT 1 FROM FILE_INDEX WHERE ori_hash=? LIMIT 1); """
                cur = conn.cursor()
                cur.execute(sql, (file_hash,))
                file = cur.fetchone()
                return True if file[0] == 1 else 0
            else:
                print("Error! when listing enc. files.")
                return []
        except Error as e:
            print(e)
            return []
        finally:
            if conn:
                conn.close()


class ProcessRequest:

    def __init__(self, dbUtils, osUtils, config):
        self.DBManager = dbUtils
        self.osUtils = osUtils
        self.config = config

    def start_encryption(self, source_folder, destination_folder):
        # 0. init location (0.1 - create the db)
        self.DBManager.create_db()
        Path(destination_folder).mkdir(parents=True, exist_ok=True)
        # 1. list all files in the folder
        filterd_file_list = self.osUtils.list_files(
            source_folder, self.DBManager.DB_FILE).values()
        # 2. insert the file details into table
        file_count = 0
        duplicate_count = 0

        for file in filterd_file_list:
            file_hash = self.osUtils.generate_hash(file)
            file_exists = self.DBManager.find_existing_file_from_hash(
                file_hash)
            fq_file_path = os.path.abspath(file)

            if not self.config['allow_duplicates'] and file_exists:
                print('ignoring the duplicate file : ' + fq_file_path)
                duplicate_count = duplicate_count + 1
            else:
                print('adding the file : ' + fq_file_path)
                if file_exists:
                    duplicate_count = duplicate_count + 1

                file_name = os.path.basename(file)
                file_size = os.path.getsize(fq_file_path)
                file_size_txt = self.osUtils.file_size_to_text(file_size)
                file_record = (file_name, fq_file_path, file_hash,
                               file_size, file_size_txt, file_exists)

                if self.DBManager.create_record(file_record):
                    file_count = file_count + 1

        print('Total duplicates found : %s out of %s.' %
              (str(duplicate_count), str(file_count)))

        # 3. read the files from table
        update_count = 0
        # 4. encrypt the files to desination
        for file_object in self.DBManager.list_new_files_from_db():
            # (ID, 'NAME', 'ORI_HASH', SIZE)
            print(file_object[2])
            enc_file_data = self.osUtils.encrypt_file(
                file_object[2], destination_folder, self.config['layer_1_passwd'])
            # 5. update the table for encrypted file hash
            if self.DBManager.update_enc_file_data(file_object[0], enc_file_data[0], enc_file_data[1]):
                update_count = update_count + 1

        print('encrypted file count : ' + str(update_count))
        
        return {"operation":'enc', "total_count": file_count , "duplicate_count":duplicate_count,"success_count":update_count,"failed_count": file_count-update_count}

    def start_decryption(self, destination_folder, new_destination_folder):
        # 1. list all files from table which were encrypted.
        dec_files_from_db = self.DBManager.list_enc_files_from_db()
        # 2. list all available files from the source folder to be decrypted
        dec_files_from_dest = self.osUtils.list_files(
            destination_folder, self.DBManager.DB_FILE)
        # 3. decrypt the matching elements
        success_file_count = 0
        ignored_file_count = 0
        
        for dec_file in dec_files_from_db:
            if dec_file[5] in dec_files_from_dest:
                enc_file_hash = self.osUtils.generate_hash(
                    dec_files_from_dest[dec_file[5]])
                # print(enc_file_hash)
                if enc_file_hash == dec_file[6]:
                    print('matching file found : ' +
                          dec_file[5] + ' starting the decrypting process..')
                    new_file_destination = os.path.abspath(
                        new_destination_folder)+dec_file[2]
                    src_file = os.path.join(destination_folder, dec_file[5])
                    # 2. decrypt the files to the given location (folder structure based on the fq_path)
                    dec_hash = self.osUtils.decrypt_file(
                        src_file, new_file_destination, self.config['layer_1_passwd'])
                    if dec_file[3] == dec_hash:
                        print('file %s was decrypted to %s.' %
                              (src_file, new_file_destination))
                        success_file_count = success_file_count + 1
                else:
                    ignored_file_count = ignored_file_count + 1

        print('Total : %s files out of %s , were successfully decrypted.' %
              (str(success_file_count), str(len(dec_files_from_db))))
        
        failed_count = len(dec_files_from_db) - (ignored_file_count + success_file_count)
        return {'operation': 'dec', 'total_from_db': len(dec_files_from_db), 'ignored_count': ignored_file_count, 'success_count': success_file_count , 'failed_count': failed_count}
