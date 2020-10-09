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


def save_all(note_path, path_html_list, not_found_list, found_multiple_list, manual_list):
    for (html_path, html_content) in path_html_list:
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
            file.truncate()

    if len(not_found_list) != 0 or len(found_multiple_list) != 0:
        error_path = os.path.splitext(note_path)[0] + "_error.txt"
        with open(error_path, 'w', encoding='utf-8') as file:
            for (old, new) in not_found_list:
                file.write(old)
                file.write('=>\n')
                file.write(new)
                file.write('\n')
                file.write('[未找到]\n\n')

            for (old, new) in found_multiple_list:
                file.write(old)
                file.write('=>\n')
                file.write(new)
                file.write('\n')
                file.write('[找到多处匹配]\n\n')

            for (old, new) in manual_list:
                file.write(old)
                file.write('=>\n')
                file.write(new)
                file.write('\n')
                file.write('[手动替换]\n\n')

            print('有问题的笔记已经保存到：{}，请手工查找并替换'.format(error_path))
    else:
        print('完美，所有注释都已经处理完毕')


def main():
    if len(sys.argv) < 3:
        print('使用方法：python3 {} <笔记文本文件> <html目录>'.format(sys.argv[0]))
        exit(0)

    note_path = sys.argv[1]
    html_dir = sys.argv[2]

    if not os.path.exists(note_path):
        print("{}笔记文件不存在".format(note_path))
        exit(0)

    if not os.path.isfile(note_path):
        print("{}笔记文件不是一个文本文件".format(note_path))
        exit(0)

    if not os.path.exists(html_dir):
        print("{}目录不存在".format(html_dir))
        exit(0)

    if not os.path.isdir(html_dir):
        print("{}不是一个目录".format(html_dir))
        exit(0)

    all_notes = read_all_notes(note_path)
    if len(all_notes) == 0:
        print("{}文件中没有找到任何笔记".format(note_path))
        exit(0)

    path_html_list = read_all_html(html_dir)
    if len(path_html_list) == 0:
        print("{}目录中没有任何html文件".format(html_dir))
        exit(0)

    not_found_list = []
    found_multiple_list = []
    manual_list = []

    for (old, new) in all_notes:
        manual1 = '手工替换'
        manual2 = '手动替换'

        if old.startswith(manual1) or old.startswith(manual2) or new.startswith(manual1) or new.startswith(manual2):
            manual_list.append((old, new))
        else:
            replace_note(old, new, path_html_list, not_found_list, found_multiple_list)

    save_all(note_path, path_html_list, not_found_list, found_multiple_list, manual_list)


if __name__ == '__main__':
    main()
