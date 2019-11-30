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
    base_dir = r'/Users/kevin/GitHub/eBookNew/中华经典名著全本全注全译丛书/wenxuan/'
    filename = r'hanzi.txt'


def replace_hanzi():
    pass


if __name__ == '__main__':
    # split_images()
    replace_hanzi()
