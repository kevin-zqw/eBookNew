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
    all_files = sorted(os.listdir(base_dir))

    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        wenxuan_split(base_dir, filename)


def insert_notes(base_dir, filename):
    path = os.path.join(base_dir, filename)

    with open(path, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()

    note_regex = r'<p class="fs">(\[\d+\])(.*?)</p>'
    header = r'<p>【<b>注释</b>】</p>'

    content = ''
    changed = False
    for line in all_lines:
        if header in line:
            continue

        matches = re.findall(note_regex, line)
        if matches:
            changed = True

            index = matches[0][0]
            note = matches[0][1]
            sup_tag = f'<sup>{index}</sup>'
            replace = f'【【{note}】】'

            if content.count(sup_tag) == 1:
                content = replace.join(content.rsplit(sup_tag, 1))
            else:
                print(line)
                content += line
        else:
            content += line

    if changed:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
            file.truncate()


def insert_all_notes():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    all_files = sorted(os.listdir(base_dir))

    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        insert_notes(base_dir, filename)


def process_h1():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    all_files = sorted(os.listdir(base_dir), reverse=True)

    h1_result = []
    vol_h3 = []
    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        path = os.path.join(base_dir, filename)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

            h3_matches = re.findall(r'<h3>(.*?)</h3>', content)
            if h3_matches:
                vol_h3.extend(h3_matches)

            h1_matches = re.findall(r'<h1>(.*?)</h1>', content)
            if h1_matches:
                if 0 < len(vol_h3):
                    h1 = h1_matches[0]
                    vol_h3.reverse()
                    h3_str = '、'.join(vol_h3)
                    h1_result.append((h1, f'{h1} {h3_str}'))

                vol_h3 = []

    print(h1_result)



def merge_all_text():
    pass
    hr_tag = r'<hr/>'


if __name__ == '__main__':
    # wenxuan_split_all()
    # insert_all_notes()
    process_h1()
