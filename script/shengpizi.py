# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys
import collections


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def split_images():
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/hanzi'
    all_images = list(filter(lambda f: f.endswith('.jpeg'), os.listdir(base_dir)))
    all_images.sort()

    list_chunks = list(chunks(all_images, 300))
    for (index, lst) in enumerate(list_chunks):
        dest_dir = base_dir + '%02d' % index
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)

        text_path = os.path.join(dest_dir, 'a_hanzi_%02d.txt' % index)
        text_list = list(map(lambda image: f'{image}：', lst))
        content = '\n'.join(text_list)
        with open(text_path, 'w', encoding='utf-8') as file:
            file.write(content)
            file.truncate()

        for image in lst:
            src_file = os.path.join(base_dir, image)
            dest_file = os.path.join(dest_dir, image)
            os.rename(src_file, dest_file)


def read_all_hanzi():
    base_dir = r'/Users/kevin/GitHub/eBookNew/sj/sj_hanzi00'
    all_txt = list(filter(lambda f: f.endswith('.txt'), os.listdir(base_dir)))

    all_hanzi = []
    for filename in all_txt:
        file_path = os.path.join(base_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.findall(r'([^\s：]*)：([^\s：]*)', line)
                if match:
                    all_hanzi.extend(match)
    return all_hanzi


def replace_hanzi():
    all_hanzi = read_all_hanzi()
    base_dir = r'/Users/kevin/GitHub/eBookNew/sj/sj_html'
    for filename in os.listdir(base_dir):
        if not filename.endswith('.xhtml'):
            continue
        file_path = os.path.join(base_dir, filename)
        with open(file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            for (image, hanzi) in all_hanzi:
                old = f'<img src="../Images/{image}" alt="" class="kindle-cn-inline-character"/>'
                new = f'<span class="font">{hanzi}</span>'
                content = content.replace(old, new)

            file.seek(0)
            file.write(content)
            file.truncate()


if __name__ == '__main__':
    # split_images()
    replace_hanzi()
