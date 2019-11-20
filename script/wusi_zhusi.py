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

    if found_count == 1 and 0 <= line_index and 0 <= text_index:
        comments.append(f"{key}【{key}：{value}】")
        index = len(comments) - 1
        placeholder = f"[[{index}]]"
        line = lines[line_index]
        lines[line_index] = line.replace(key, placeholder, 1)

        return True
    else:
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


def read_all_comments():
    path = r'/Users/kevin/GitHub/eBookMake/wusi/note/part0026.xhtml'

    all_comments = []
    comment_regex = r'<li><p id="(.*?)">(.*?)<a href="\.\./Text/(.*)#(.*?)">↩</a></p></li>'
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            is_comment = re.search(comment_regex, line)
            if is_comment:
                all_comments.append(is_comment)

    print("Comments count: ", len(all_comments))
    return all_comments


if __name__ == '__main__':
    base_dir = r'/Users/kevin/GitHub/eBookMake/wusi'
    comment_list = read_all_comments()

    for comment in comment_list:
        # group 1: id; 2: text; 3: filename; 4: href
        item_id = comment.group(1)
        text = comment.group(2)
        filename = comment.group(3)
        href = comment.group(4)

        raw_item_id = item_id.replace('-', r'\-')
        raw_href = href.replace('-', r'\-')

        file_path = os.path.join(base_dir, filename)
        with open(file_path, 'r+', encoding='utf-8') as file:
            result_text = file.read()

            replace_regex = r'(<p><a class="amzn" epub:type="noteref" href="\.\./Text/part\d+\.xhtml#.*?">.*?</a>.*?)<a class="Note Number" id="' + f'{raw_href}' + r'" name=".*?" href="\.\./Text/part\d+.xhtml#' + f'{raw_item_id}' + r'">\d+</a>(.*?</p>)'
            if re.search(replace_regex, result_text):
                sub = r'\1<span class="note-in-note">' + f'〔{text}〕' + r'</span>\2'
                result_text = re.sub(replace_regex, sub, result_text)
            else:
                result_text = result_text.replace('</body>', f'<p>[[{item_id}:{href}]]{text}</p>\n</body>')

            file.seek(0)
            file.write(result_text)
            file.truncate()

