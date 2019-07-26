# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


new_line = '\n'
comment_need_merge_regex = r'(<p class="note1"><a id=".*?" href="\.\./Text/[\w\d]*?\.xhtml#.*?">.*?</a>.*?</p>)\s+<p class="normaltext.*?">'
merge_replace_regex = r'(<p class="note1"><a id=".*?" href="\.\./Text/[\w\d]*?\.xhtml#.*?">.*?</a>)(.*?)(</p>)'
comment_regex = r'<p class="note1"><a id=".*?" href="\.\./Text/[\w\d]*?\.xhtml#(.*?)">.*?</a>(.*?)</p>'
merge_regex = r'<p class="normaltext.*?">\s*(.*?)</p>'
merge_end_regex1 = r'<p.*?><br/></p>'
merge_end_regex2 = r'<p.*?>【.*?】</p>'


def merge_comment(path):
    need_merge_lines = []
    with open(path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        need_merge_lines = re.findall(comment_need_merge_regex, html_content)

    if len(need_merge_lines) == 0:
        return

    print(path)

    all_lines = []
    with open(path, 'r', encoding='utf-8') as file:
        is_merging = False
        merging_line = ''

        for line in file:
            if is_merging:
                is_another_comment = 0 < len(re.findall(comment_regex, line))
                is_end1 = 0 < len(re.findall(merge_end_regex1, line))
                is_end2 = 0 < len(re.findall(merge_end_regex2, line))

                subtext = re.findall(merge_regex, line)
                need_merge = 0 < len(subtext)

                if need_merge:
                    if 1 < len(subtext):
                        raise Exception('Found more than 1 merge text')
                    replace = r'\1\2<br/>　　' + subtext[0] + r'\3'
                    merging_line = re.sub(merge_replace_regex, replace, merging_line)
                elif is_end1 or is_end2:
                    is_merging = False
                    all_lines.append(merging_line)
                    all_lines.append(line)
                elif is_another_comment:
                    if any(item for item in need_merge_lines if line.strip() == item):
                        all_lines.append(merging_line)
                        is_merging = True
                        merging_line = line
                    else:
                        is_merging = False
                        all_lines.append(merging_line)
                        all_lines.append(line)
                elif 0 < len(line.strip()):
                    all_lines.append(line)
            else:
                if any(item for item in need_merge_lines if line.strip() == item):
                    is_merging = True
                    merging_line = line
                else:
                    all_lines.append(line)

    with open(path, 'w', encoding='utf-8') as file:
        file.writelines(all_lines)


def process_comment(path, replace):
    print(os.path.basename(path))

    all_text = ''
    with open(path, 'r', encoding='utf-8') as file:
        all_text = file.read()

    all_comments = re.findall(r'<p>1(.*?)</p>', all_text)
    if len(all_comments) == 0:
        return

    start_index = 0
    insert_index = 1
    for comment in all_comments:
        p_comm = '<p>1{}</p>'.format(comment)
        if not replace:
            end_index = all_text.find(p_comm)
        all_text = all_text.replace(p_comm, '')

        pair_array = []
        last_index = 0
        comment_key = '1'
        for match in re.finditer(r'[，。？！—、：<；>’”](\d{1,2})[^\d]', comment):
            comment_value = comment[last_index:match.start()+1]
            # print(comment_key, '=>', comment_value)
            pair_array.append((comment_key, comment_value))

            last_index = match.end()-1
            comment_key = match.group(1)

        # add the last comment
        # print(comment_key, '=>', comment[last_index:])
        pair_array.append((comment_key, comment[last_index:]))

        index = 0
        for key, value in pair_array:
            curr_index = int(key)
            if curr_index != index + 1:
                print(key, '=>', value)
            index = curr_index

        if replace:
            for key, value in pair_array:
                pattern_replace = r'([^\d，。？！—、：<；>]){}([，。？！—、：；’”<])'.format(key)
                repl_replace = r'\1【【{}||{}】】\2'.format(insert_index, value)
                insert_index += 1
                all_text = re.sub(pattern_replace, repl_replace, all_text, 1)
        else:
            search_text = all_text[start_index:end_index]
            start_index = end_index
            inserts = re.findall(r'[^\d，。？！—、：<；>](\d{1,2})[，。？！—、：；’”<]', search_text)
            if len(inserts) != len(pair_array):
                print(inserts)
                print(pair_array[0])
            else:
                comm_indexes = []
                for i, ins in enumerate(inserts):
                    comm_indexes.append(pair_array[i][0])
                if comm_indexes != inserts:
                    print(inserts)
                    print(pair_array[0])
    with open(path, 'w', encoding='utf-8') as file:
        file.write(all_text)


if __name__ == '__main__':
    base_dir = r'/Users/kevin/GitHub/eBookNew/html'

    # merge_comment(r'/Users/kevin/GitHub/eBookNew/html/part0028.xhtml')
    for filename in os.listdir(base_dir):
        if not filename.endswith('.xhtml'):
            continue

        file_path = os.path.join(base_dir, filename)
        merge_comment(file_path)
        # process_comment(file_path, True)
