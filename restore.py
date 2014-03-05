#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass
import sys
import os
PATH = sys.path[0]
sys.path.append('%s/lib' % PATH)
import utilit

LOG_DIR = 'log'


def find_line(address):
    files = get_files_list()
    file_data = find_text_in_files(address, files)
    if not file_data:
        return None
    line = find_text_in_line(address, file_data.split('\n'))
    return line


def find_text_in_files(s, files):
    file_data = None
    for fl in files:
        file_data = file_read("%s/%s/%s" % (PATH, LOG_DIR, fl))
        if s in file_data:
            break
        file_data = None
    return file_data


def find_text_in_line(s, lines):
    for line in lines:
        if s in line:
            return line
    return None


def file_read(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data


def get_files_list():
    return os.listdir('%s/%s/' % (PATH, LOG_DIR))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("error: need address")
    address = sys.argv[1]
    pwd = getpass("secret: ")
    line = find_line(address)
    if not line:
        exit("error: no find address in log")
    log_data, log_b58_encrypted_key, log_address, log_secret = line.split(" ")
    if address != log_address:
        exit("error: fing address not unequal set address")
    if utilit.str_to_base58(utilit.dhash(utilit.dhash(pwd))) != log_secret:
        exit("error: wrong secret")
    b58_key = utilit.decrypted(pwd, log_b58_encrypted_key)
    print "key", b58_key
