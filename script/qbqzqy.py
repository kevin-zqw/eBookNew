# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


def wenxuan_split(base_dir, filename):
    dest_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html_split'
    src_path = os.path.join(base_dir, filename)
    name_no_ext = os.path.splitext(filename)[0]
    extension = '.xhtml'

    content = ''
    with open(src_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if '<h5' in content:
        body = '<body>'
        prefix = content.split(body)[0] + body + '\n'
        postfix = '</body>\n</html>'

        h5 = '<h5'
        parts = content.split(h5)
        last_index = len(parts) - 1
        for (index, pt) in enumerate(parts):
            html = ''
            if index == 0:
                html = pt + postfix
            elif index == last_index:
                html = prefix + h5 + pt
            else:
                html = prefix + h5 + pt + postfix

            index_str = '_%03d' % index
            dest_name = name_no_ext + index_str + extension
            dest_path = os.path.join(dest_dir, dest_name)
            with open(dest_path, 'w', encoding='utf-8') as file:
                file.write(html)
                file.truncate()
    else:
        dest_name = name_no_ext + '_000' + extension
        dest_path = os.path.join(dest_dir, dest_name)
        with open(dest_path, 'w', encoding='utf-8') as file:
            file.write(content)
            file.truncate()


def wenxuan_split_all():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    all_files = os.listdir(base_dir)
    all_files.sort()

    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        wenxuan_split(base_dir, filename)


if __name__ == '__main__':
    wenxuan_split_all()
