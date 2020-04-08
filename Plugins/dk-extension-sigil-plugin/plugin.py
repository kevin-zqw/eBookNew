# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from __future__ import unicode_literals, division, absolute_import, print_function

import os
import sys
import zipfile

from compatibility_utils import PY2, unicode_str
from unipath import pathof

from utilities import expanduser, file_open


_DEBUG_ = False

XMLFILE = 'duokan-extension.xml'

def run(bk):
    if 'META-INF/{}'.format(XMLFILE) in bk._w.other:
        msg = 'The {} file is already present. Please delete it before trying to add another'.format(XMLFILE)
        print(msg)
        return 0

    if _DEBUG_:
        print('Python sys.path: {}\n'.format(sys.path))

    data = '<?xml version="1.0" encoding="UTF-8" ?>\n<duokan-extension version="2.4.0">\n</duokan-extension>'

    if _DEBUG_:
        print('Internal epub href: META-INF/{}\n'.format(XMLFILE))

    bk.addotherfile('META-INF/{}'.format(XMLFILE), data)

    return 0

def main():
    print ('I reached main when I should not have\n')
    return -1

if __name__ == "__main__":
    sys.exit(main())
