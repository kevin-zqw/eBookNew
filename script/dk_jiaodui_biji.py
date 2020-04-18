# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


def read_all_notes(note_path):
    notes = []
    with open(note_path, 'r', encoding='utf-8') as file:
        content = file.read()
        notes = re.findall(r'\d\d\d\d-\d\d-\d\d\n([^\n]+)\n注: ([^\n]+)\n', content)
    return notes


def read_all_html(html_dir):
    result = []
    for filename in os.listdir(html_dir):
        if not filename.endswith('.xhtml'):
            continue
        file_path = os.path.join(html_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            result.append((file_path, html_content))
    return result


def replace_note(old, new, path_html_list, not_found_list, found_multiple_list):
    match_count = 0
    match_index = -1
    replace_path = ''
    replace_content = ''
    for index, (html_path, html_content) in enumerate(path_html_list):
        count = html_content.count(old)
        match_count += count
        if count == 1:
            match_index = index
            replace_path = html_path
            replace_content = html_content

    if match_count <= 0:
        not_found_list.append((old, new))
    elif 1 < match_count:
        found_multiple_list.append((old, new))
    else:
        if 0 <= match_index < len(path_html_list):
            replace_content = replace_content.replace(old, new)
            path_html_list[match_index] = (replace_path, replace_content)


def save_all(note_path, path_html_list, not_found_list, found_multiple_list):
    for (html_path, html_content) in path_html_list:
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
            file.truncate()

    if len(not_found_list) != 0 or len(found_multiple_list) != 0:
        error_path = os.path.splitext(note_path)[0] + "_error.txt"
        with open(error_path, 'w', encoding='utf-8') as file:
            for (old, new) in not_found_list:
                file.write(old)
                file.write('\n')
                file.write(new)
                file.write('\n')
                file.write('[未找到]\n\n')

            for (old, new) in found_multiple_list:
                file.write(old)
                file.write('\n')
                file.write(new)
                file.write('\n')
                file.write('[找到多处匹配]\n\n')


def main():
    if len(sys.argv) < 3:
        print('usage: python3 {} <note_txt> <html_dir>'.format(sys.argv[0]))
        exit(0)

    note_path = sys.argv[1]
    html_dir = sys.argv[2]

    if not os.path.exists(note_path):
        print("{} doesn't exists".format(note_path))
        exit(0)

    if not os.path.isfile(note_path):
        print("{} is not a file".format(note_path))
        exit(0)

    if not os.path.exists(html_dir):
        print("{} doesn't exists".format(html_dir))
        exit(0)

    if not os.path.isdir(html_dir):
        print("{} is not a dir".format(html_dir))
        exit(0)

    all_notes = read_all_notes(note_path)
    if len(all_notes) == 0:
        print("No notes found in {}".format(note_path))
        exit(0)

    path_html_list = read_all_html(html_dir)
    if len(path_html_list) == 0:
        print("No html file found in {}".format(html_dir))
        exit(0)

    not_found_list = []
    found_multiple_list = []

    for (old, new) in all_notes:
        replace_note(old, new, path_html_list, not_found_list, found_multiple_list)

    save_all(note_path, path_html_list, not_found_list, found_multiple_list)


if __name__ == '__main__':
    main()
