#!/usr/bin/python
'''
	Program will compare all files content from a given arguments
	by calculating hashes with specified method.
    See usage for available methods.
'''

import sys
import os
import hashlib
import collections
import argparse

File = collections.namedtuple(
    'File', ['full_file_name', 'hash', 'hash_method_name'])


if __name__ == '__main__':

    # create arguments parser
    parser = argparse.ArgumentParser(
        description='Hello, we will compare hashes for files!')
    parser.add_argument(
        'filename',
        nargs='+',
        help='files to calculate hashes')
    parser.add_argument(
        '--hash_method',
        default='sha256',
        nargs='?',
        choices=('sha1', 'sha256'),
        help='hash method name')
    args = parser.parse_args()

    # here will be result list of File objects
    files = []

    # fast checking files exists
    all_files_exists = True
    for filename in args.filename:
        if not os.path.isfile(filename):
            print('[-!-] File not found: {}'.format(filename))
            all_files_exists = False

    if not all_files_exists:
        sys.exit('[-!-] ERROR: Check filenames and try again.', 1)

    # calculate hashes for every file
    print('[---] Calculating hashes for {} file(s). Please wait.'.format(len(args.filename)))
    for filename in args.filename:
        if os.path.isfile(filename):
            try:
                                # open file and calculate hash
                with open(filename, 'br') as f:
                    hash_method_name = args.hash_method
                    hash_method = getattr(hashlib, hash_method_name)
                    hash = hash_method(f.read())
            except Exception as e:
                                # exit if any exception occur
                sys.exit('[-!-] ERROR: {}'.format(e), 1)

                # add result
            files.append(
                File(
                    full_file_name=filename,
                    hash_method_name=hash_method_name,
                    hash=hash.hexdigest()
                )
            )

    # print results
    for file in files:
        print('{} {} {}'.format(
            file.hash, file.hash_method_name, file.full_file_name))

    # check that all hashes are equal
    count_diff_hashes = len(list(set([file.hash for file in files])))
    # should be only one hash, if all files have the same content
    if count_diff_hashes == 1:
        print('[---] OK. All files has the same content.')
    else:
        print('*'*50)
        print('      WRONG. Different hash found !     ')
        print('*'*50)
