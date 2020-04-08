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
ENCRYPTIONFILE = 'encryption.xml'

def run(bk):
    data = '<?xml version="1.0" encoding="UTF-8" ?>\n<duokan-extension version="2.4.0">\n</duokan-extension>\n'

    if 'META-INF/{}'.format(XMLFILE) not in bk._w.other:
        bk.addotherfile('META-INF/{}'.format(XMLFILE), data)

    encryption_data = """\
<?xml version="1.0" encoding="UTF-8" ?>
<encryption xmlns="urn:oasis:names:tc:opendocument:xmlns:container" xmlns:enc="http://www.w3.org/2001/04/xmlenc#" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
    <enc:EncryptedKey Id="KEY">
        <enc:EncryptionMethod Algorithm="http://www.w3.org/2001/04/xmlenc#rsa-1_5" />
        <ds:KeyInfo>
            <ds:KeyName>DuoKan.Inc</ds:KeyName>
        </ds:KeyInfo>
        <enc:CipherData>
            <enc:CipherValue>SD0O9fuI+cntUXTuNiyfCg3nIRAHDMVURJlE3my14SUzo4Kv/x0k42tthYJledwxSXf4rVguS99Mp+sGiWGQvHOkeUlH6/iKvIZ5PjwgKl0=</enc:CipherValue>
        </enc:CipherData>
    </enc:EncryptedKey>
    <enc:EncryptedData Id="DATA0">
        <enc:EncryptionMethod Algorithm="http://www.w3.org/2001/04/xmlenc#aes128-ctr" />
        <ds:KeyInfo>
            <ds:RetrievalMethod URI="#KEY" Type="http://www.w3.org/2001/04/xmlenc#EncryptedKey" />
        </ds:KeyInfo>
        <enc:CipherData>
            <enc:CipherReference URI="OEBPS/Styles/dkagent.css" />
        </enc:CipherData>
    </enc:EncryptedData>

</encryption>
"""

    if 'META-INF/{}'.format(ENCRYPTIONFILE) not in bk._w.other:
        bk.addotherfile('META-INF/{}'.format(ENCRYPTIONFILE), encryption_data)

    return 0

def main():
    print ('I reached main when I should not have\n')
    return -1

if __name__ == "__main__":
    sys.exit(main())
