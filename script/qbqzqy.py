# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys
import collections


def wenxuan_split(base_dir, dest_dir, filename):
    print(filename)

    src_path = os.path.join(base_dir, filename)
    name_no_ext = os.path.splitext(filename)[0]
    extension = '.xhtml'

    with open(src_path, 'r', encoding='utf-8') as file:
        content = file.read()
        file.seek(0)
        all_lines = file.readlines()

    h1_tag = '<h1'
    h2_tag = '<h2'
    h3_tag = '<h3'

    count_h1 = content.count(h1_tag)
    count_h2 = content.count(h2_tag)
    count_h3 = content.count(h3_tag)

    body_start = '<body>'
    body_end = '</body>'
    prefix = content.split(body_start)[0] + body_start + '\n'
    postfix = f'{body_end}\n</html>'

    need_split = True
    if count_h1 + count_h2 + count_h3 <= 1:
        need_split = False
    if '"chapter"' in content:
        need_split = False

    if need_split:
        sub_lines = []
        body_start_matched = False
        header_matched = False
        index = 1
        for line in all_lines:
            if body_start in line:
                sub_lines = []
                body_start_matched = True
                continue

            if not body_start_matched:
                continue

            if body_end in line:
                index_str = '_%03d' % index
                index += 1
                dest_name = name_no_ext + index_str + extension
                dest_path = os.path.join(dest_dir, dest_name)
                with open(dest_path, 'w', encoding='utf-8') as file:
                    file.write(prefix + ''.join(sub_lines) + postfix)
                    file.truncate()
                break
            elif h1_tag in line or h2_tag in line or h3_tag in line:
                if header_matched:
                    index_str = '_%03d' % index
                    index += 1
                    dest_name = name_no_ext + index_str + extension
                    dest_path = os.path.join(dest_dir, dest_name)
                    with open(dest_path, 'w', encoding='utf-8') as file:
                        file.write(prefix + ''.join(sub_lines) + postfix)
                        file.truncate()
                    sub_lines = [line]
                else:
                    header_matched = True
                    sub_lines.append(line)
            else:
                sub_lines.append(line)
    else:
        dest_path = os.path.join(dest_dir, filename)
        with open(dest_path, 'w', encoding='utf-8') as file:
            file.write(content)
            file.truncate()


def wenxuan_split_all():
    base_dir = r'/Users/orcbit/Stuff/eBookNew/中华经典名著全本全注全译丛书/shisanjing/html'
    all_sub_dirs = [name for name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, name))]
    for dir_path in all_sub_dirs:
        wenxuan_split_dir(os.path.join(base_dir, dir_path))
        break


def wenxuan_split_dir(dir_path):
    all_files = sorted(os.listdir(dir_path))

    dest_dir = os.path.join(dir_path, 'html_split')
    if os.path.exists(dest_dir) and os.path.isdir(dest_dir):
        shutil.rmtree(dest_dir)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        wenxuan_split(dir_path, dest_dir, filename)


def insert_notes(base_dir, filename):
    path = os.path.join(base_dir, filename)

    with open(path, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()

    note_regex = r'<p class="fuck">(.*?)___(.*?)</p>'
    header = r'>【注释】<'

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
            sup_tag = f'<span class="math-super">{index}</span>'
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
    base_dir = r'/Users/orcbit/Stuff/eBookNew/中华经典名著全本全注全译丛书/shisanjing/html/13_erya'
    all_files = sorted(os.listdir(base_dir))

    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        insert_notes(base_dir, filename)


def process_heading_1():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    all_files = sorted(os.listdir(base_dir), reverse=True)

    h1_result = []
    vol_h3 = []
    h3_temp_files = []
    need_delete_h3_files = []
    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        path = os.path.join(base_dir, filename)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

            # process h1
            h3_matches = re.findall(r'<h3>(.*?)</h3>', content)
            if h3_matches:
                vol_h3.extend(h3_matches)
                h3_temp_files.append(filename)

            h1_matches = re.findall(r'<h1>(.*?)</h1>', content)
            if h1_matches:
                if 0 < len(vol_h3):
                    h1 = h1_matches[0]
                    vol_h3.reverse()
                    h3_str = '、'.join(vol_h3)
                    h1_result.append((h1, f'{h1} {h3_str}', filename))
                    if 1 == len(vol_h3):
                        need_delete_h3_files.extend(h3_temp_files)

                vol_h3 = []
                h3_temp_files = []

    for (old, new, filename) in h1_result:
        old_h = f'<h1>{old}</h1>'
        new_h = f'<h1>{new}</h1>'

        path = os.path.join(base_dir, filename)
        with open(path, 'r+', encoding='utf-8') as file:
            content = file.read()
            content = content.replace(old_h, new_h)

            if filename in need_delete_h3_files:
                content = re.sub(r'<h3>.*?</h3>', '', content)

            file.seek(0)
            file.write(content)
            file.truncate()


def process_heading_5():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    all_files = sorted(os.listdir(base_dir), reverse=False)

    h5_result = []
    author = None
    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        path = os.path.join(base_dir, filename)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

            # process h1
            h1_matches = re.findall(r'<h1>(.*?)</h1>', content)
            if h1_matches:
                author = None

            h3_matches = re.findall(r'<h3>(.*?)</h3>', content)
            if h3_matches:
                author = None

            # process author and articles
            h4_authors = re.findall(r'<h4>(.*?)</h4>', content)
            if h4_authors:
                author = h4_authors[0]

            h5_articles = re.findall(r'<h5>(.*?)</h5>', content)
            if h5_articles and author:
                article = h5_articles[0]
                h5_result.append((article, f'{article}（{author}）', filename))

    for (old, new, filename) in h5_result:
        old_h = f'<h5>{old}</h5>'
        new_h = f'<h5>{new}</h5>'

        path = os.path.join(base_dir, filename)
        with open(path, 'r+', encoding='utf-8') as file:
            content = file.read()
            content = content.replace(old_h, new_h)

            file.seek(0)
            file.write(content)
            file.truncate()


def rename_all_files():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    all_files = sorted(os.listdir(base_dir))

    vol_index = 0
    sec_index = 0
    file_index = 0
    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        path = os.path.join(base_dir, filename)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

        if r'<h1>卷' in content:
            vol_index += 1
            sec_index = 0
            file_index = 0
        elif r'<h3>' in content:
            sec_index += 1
            file_index = 0

        new_name = 'v%02d_s%02d_p%02d.xhtml' % (vol_index, sec_index, file_index)
        os.rename(os.path.join(base_dir, filename), os.path.join(base_dir, new_name))
        file_index += 1


def move_no_need_merge_files():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    dest_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html_no_merge'

    yiwen = r'<p>【<b>译文</b>】</p>'
    hr = r'<hr/>'
    h6 = r'<h6'
    poem_title = r'<p class="center"><b'
    title_regex = r'<h\d.*?[^一]首'

    for filename in os.listdir(base_dir):
        if not filename.endswith('.xhtml'):
            continue

        path = os.path.join(base_dir, filename)
        dest_path = os.path.join(dest_dir, filename)

        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

        if content.count(yiwen) != content.count(hr):
            print(filename)

        need_move = False
        if h6 in content or poem_title in content:
            need_move = True
        if content.count(yiwen) <= 1 or content.count(hr) <= 1:
            need_move = True
        title_match = re.findall(title_regex, content)
        if title_match and 0 < len(title_match):
            need_move = True

        if need_move:
            os.rename(path, dest_path)


def merge_all_text():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    all_files = sorted(os.listdir(base_dir))

    yiwen = r'<p>【<b>译文</b>】</p>'
    hr = r'<hr/>'
    body_end = r'</body>'
    html_end = r'</html>'
    origin_placeholder = '<p class="origin"><br/></p>\n'

    for filename in all_files:
        if not filename.endswith('.xhtml'):
            continue

        prefix = []
        origin = []
        translate = []

        merge_started = False
        is_translate = False

        path = os.path.join(base_dir, filename)
        with open(path, 'r', encoding='utf-8') as file:
            all_lines = file.readlines()
            for line in all_lines:
                if hr in line:
                    merge_started = True
                    is_translate = False
                    if 0 == len(origin):
                        origin.append(origin_placeholder)
                    continue
                if yiwen in line:
                    merge_started = True
                    is_translate = True
                    if 0 == len(translate):
                        translate.append(line)
                    continue

                if body_end in line:
                    break

                if merge_started:
                    if is_translate:
                        translate.append(line)
                    else:
                        origin.append(line)
                else:
                    prefix.append(line)

        result = []
        result.extend(prefix)
        result.extend(origin)
        result.extend(translate)
        result.append(body_end + '\n')
        result.append(html_end + '\n')

        with open(path, 'w', encoding='utf-8') as file:
            file.write(''.join(result))
            file.truncate()


def process_center_block():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    center_tag = r'class="center"'
    title_tag = r'class="intitle"'
    all_files = sorted(os.listdir(base_dir))

    for filename in all_files:
        file_path = os.path.join(base_dir, filename)

        with open(file_path, 'r+', encoding='utf-8') as file:
            all_lines = file.readlines()
            title_indexes = []
            poem_indexes = []

            line_count = len(all_lines)
            for (index, line) in enumerate(all_lines):
                is_current_match = center_tag in line
                is_previous_match = False
                is_next_match = False
                previous = index - 1
                next = index + 1
                if 0 <= previous:
                    is_previous_match = center_tag in all_lines[previous]
                if next < line_count:
                    is_next_match = center_tag in all_lines[next]

                if is_current_match:
                    if is_previous_match or is_next_match:
                        poem_indexes.append(index)
                    else:
                        title_indexes.append(index)

            need_save = 0 < len(title_indexes) or 0 < len(poem_indexes)
            for index in title_indexes:
                line = all_lines[index]
                all_lines[index] = line.replace(center_tag, title_tag)

            if need_save:
                file.seek(0)
                file.writelines(all_lines)
                file.truncate()


def check_merge():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/html'
    all_files = sorted(os.listdir(base_dir))
    for filename in all_files:
        file_path = os.path.join(base_dir, filename)
        with open(file_path, 'r+', encoding='utf-8') as file:
            contents = file.read()
        if contents.count('yuanwen.png') <= 1 and contents.count('yiwen.png') <= 1:
            os.remove(file_path)


if __name__ == '__main__':
    wenxuan_split_all()
    # insert_all_notes()
    # process_heading_1()
    # process_heading_5()
    # rename_all_files()
    # move_no_need_merge_files()
    # merge_all_text()
    # process_center_block()
    # check_merge()
