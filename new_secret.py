#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getpass import getpass
import sys

PATH = sys.path[0]
sys.path.append('%s/lib' % PATH)
import utilit

if __name__ == "__main__":
    pwd1, pwd2 = 1, 2
    while pwd1 != pwd2:
        pwd1 = getpass("secret: ")
        pwd2 = getpass("secret2: ")
    print utilit.str_to_base58(utilit.dhash(utilit.dhash(pwd1)))

