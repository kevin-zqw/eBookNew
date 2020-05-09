# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys
import collections


def split_html(base_dir, filename):
    file_path = os.path.join(base_dir, filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        file.seek(0)
        all_lines = file.readlines()

    split_tag = r'----split----'

    if split_tag not in content:
        return

    print('split', filename)

    body_start = '<body>'
    body_end = '</body>'
    prefix = content.split(body_start)[0] + body_start + '\n'
    postfix = f'{body_end}\n</html>'

    sub_lines = []
    body_start_matched = False
    tag_matched = False
    index = 1
    for line in all_lines:
        if body_start in line:
            sub_lines = []
            body_start_matched = True
            continue

        if not body_start_matched:
            continue

        if body_end in line:
            save_split_file(base_dir, filename, index, prefix, postfix, sub_lines)
            index += 1
            break
        elif split_tag in line:
            if tag_matched:
                save_split_file(base_dir, filename, index, prefix, postfix, sub_lines)
                index += 1
            else:
                tag_matched = True
                sub_lines.append(line)
        else:
            sub_lines.append(line)


def save_split_file(base_dir, filename, index, prefix, postfix, lines):
    name_no_ext = os.path.splitext(filename)[0]
    extension = '.xhtml'

    index_str = '_%03d' % index

    dest_name = name_no_ext + index_str + extension
    dest_path = os.path.join(base_dir, dest_name)
    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(prefix + ''.join(lines) + postfix)
        file.truncate()


def main():
    base_dir = r'/Users/kevin/GitHub/eBookNew/Hemingway/Text'
    all_files = sorted(os.listdir(base_dir))

    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        split_html(base_dir, filename)


if __name__ == '__main__':
    main()
