# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


new_line = '\n'


def search_replace_comment(lines, comments, key, value):
    found_count = 0
    line_index = -1
    text_index = -1

    body = "<body"
    end_1 = "【校】"
    end_2 = "【注】"

    body_reached = False
    end_1_reached = False
    end_2_reached = False

    for i, line in enumerate(lines):
        if body in line:
            body_reached = True
        if "<h" in line:
            end_1_reached = False
            end_2_reached = False
        if end_1 in line:
            end_1_reached = True
        if end_2 in line:
            end_2_reached = True

        if not body_reached:
            continue
        if end_1_reached or end_2_reached:
            continue

        if key in line:
            found_count += 1
            line_index = i
            text_index = 0

    global succeed_count, failed_count
    if found_count == 1 and 0 <= line_index and 0 <= text_index:
        succeed_count += 1
        comments.append(f"{key}【{key}：{value}】")
        index = len(comments) - 1
        placeholder = f"[[{index}]]"
        line = lines[line_index]
        lines[line_index] = line.replace(key, placeholder, 1)

        return True
    else:
        failed_count += 1
        print("bad:", key, value)
        return False


def process_comment(path):
    print(os.path.basename(path))

    all_lines = []
    comments = []

    with open(path, 'r', encoding='utf-8') as file:
        last_is_comment = False
        for line in file:
            is_comment = re.search(r'<p class="bodytext"><b>(.*?)：</b>(.*?)</p>', line)
            if is_comment:
                last_is_comment = True
                key = is_comment.group(1)
                value = is_comment.group(2)
                is_succeed = search_replace_comment(all_lines, comments, key, value)
                if not is_succeed:
                    all_lines.append(line)
            else:
                if 0 < len(line.strip()):
                    last_is_comment = False

                if not last_is_comment:
                    all_lines.append(line)

    result_text = "".join(all_lines)
    for i, c in enumerate(comments):
        placeholder = f"[[{i}]]"
        result_text = result_text.replace(placeholder, c)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(result_text)


succeed_count = 0
failed_count = 0

if __name__ == '__main__':
    base_dir = r'/Users/kevin/GitHub/eBookMake/wangwei'
    for filename in os.listdir(base_dir):
        if not filename.endswith('.xhtml'):
            continue

        file_path = os.path.join(base_dir, filename)
        process_comment(file_path)

    print("succeed: ", succeed_count)
    print("failed: ", failed_count)
