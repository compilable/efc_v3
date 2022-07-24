#!/usr/bin/env python3

from distutils.log import error
import errno
import hashlib
import os
import sys
import argparse
import pathlib

from init import DBUtils, OSUtils, ProcessRequest


def start(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-operation', choices=['e', 'd'], required=True, default='e',
                        help='operation (e for encrypt, d for decrypt) (default : e)')
    parser.add_argument('-src', required=True, default='e', type=pathlib.Path,
                        help='source folder location.')
    parser.add_argument('-dest', required=False, default='.', type=pathlib.Path,
                        help='destination folder location.')
    parser.add_argument('-index-file', required=False, default='./.db',
                        help='password to encrypt the `index file`. (optional)')
    parser.add_argument('-index-password', required=False, default='e',
                        help='index file name and location (optional) an index file will be created with `.db` on the source location.')
    parser.add_argument('-index-delete', required=False, default=True, choices=['yes', 'no'],
                        help='delete the decrypted index file.') 
    parser.add_argument('-data-password', required=True, default='e',
                        help='password to encrypt the `file content`..')
    parser.add_argument('-restore', required=False, default='.', type=pathlib.Path,
                        help='restore folder location (optional) ')
    parser.add_argument('-allow-duplicate', choices=['yes', 'no'],  required=False, default='no',
                        help='allow duplicate files during encryption process (optional). (default : no)')
    parser.add_argument('-random-names', choices=['yes', 'no'], required=False, default='no',
                        help='generate random names for files (optional). (default : no)')
    parser.add_argument('-ignore-types', required=False, default=[],
                        help='list of file types (extensions) to ignore. (optional)')

    args = parser.parse_args()
    print(args)
    deligate_operation(args)


def deligate_operation(args):

    if os.path.isdir(args.src) and os.path.exists(args.src):
        print('source data : ', args.src)
    else:
        print('source data location not exists : ', args.src)
        exit()

    options = validate_options(args)
    osUtils = OSUtils('ev3', options.ignore_types.split(","))
    process_config = {
        "layer_2_passwd": options.index_password,
        "layer_1_passwd": options.data_password,
        "allow_duplicates": True if options.allow_duplicate.lower() == 'yes' else False,
        "delete_index": True if options.index_delete.lower() == 'yes' else False
    }
    print(process_config)
    process_user_request = ProcessRequest(
        DBUtils(options.index_file), osUtils, process_config)

    if args.operation == 'e':
        process_user_request.start_encryption(options.src, options.dest)
    else:
        process_user_request.start_decryption(
            options.src, options.restore, options.index_file, options.index_delete)


def validate_options(args):

    error_text = 'destination folder coudnt be created : ' + \
        str(args.dest) if args.operation == 'e' else 'restore folder coudnt be created : ' + str(args.restore)
    success_text = 'destination folder created : ' + \
        str(args.dest) if args.operation == 'e' else 'restore folder created : ' + \
        str(args.restore)

    # create destinat if not exists & check
    try:
        if args.operation == 'e':
            os.makedirs(args.dest)
        else:
            os.makedirs(args.restore)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print(error_text)
            exit()

    if os.path.exists(args.dest):
        print(success_text)
    else:
        print(error_text)
        exit()

    # add pepper and generate sha512 hash
    args.data_password = add_pepper(args.data_password)
    args.index_password = add_pepper(args.index_password)

    return args


def add_pepper(text):
    return (hashlib.sha512(''.join(str([chr(i) for i in range(128)])).encode("utf-8")+text.encode("utf-8")).digest()).decode("unicode_escape")


if __name__ == "__main__":
    start(sys.argv[1:])
