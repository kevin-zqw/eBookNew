# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys

pattern_duokan_comment = r'(【【([^【】]*?)】】)'
duokan_comment_ref_template = '<sup><a style="text-decoration:none!important;color:black;" class="duokan-footnote" href="#footnote{}" id="note{}"><img alt="" src="../Images/note.png"/></a></sup>'
duokan_comment_define_template = '<li class="duokan-footnote-item" id="footnote{}">\n<p class="footnote"><a style="text-decoration:none!important;color:black;" href="#note{}">◎</a>{}​​​​​​​​​</p>\n</li>\n\n'
duokan_comment_start = '\n\n<div>\n<hr class="xian"/>\n</div>\n\n<ol class="duokan-footnote-content">\n\n'
duokan_comment_end = '</ol>\n\n'


def process_comment(file_path):
    with open(file_path, 'r+', encoding='utf-8') as f:
        result_lines = []

        duokan_comment = []
        comment_index = 1
        for line in f.readlines():
            comment_groups = re.findall(pattern_duokan_comment, line)
            for comment_tag, comment_text in comment_groups:
                line = line.replace(comment_tag, duokan_comment_ref_template.format(comment_index, comment_index))
                duokan_comment.append(duokan_comment_define_template.format(comment_index, comment_index, comment_text))
                comment_index += 1

            if '</body>' not in line and '</html>' not in line:
                result_lines.append(line)

        f.seek(0)
        f.write(''.join(result_lines))

        if len(duokan_comment) > 0:
            f.write(duokan_comment_start)
            for comment in duokan_comment:
                f.write(comment)
            f.write(duokan_comment_end)

        f.write('</body>'+'\n')
        f.write('</html>'+'\n')

        f.truncate()


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print('usage: python3 {} <dir>'.format(sys.argv[0]))
    #     exit(0)
    # dir_path = sys.argv[1]
    dir_path = r'/Users/orcbit/Stuff/eBookNew/中华经典名著全本全注全译丛书/shisanjing/html_split'

    for filename in os.listdir(dir_path):
        if not filename.endswith('.xhtml'):
            continue

        file_path = os.path.join(dir_path, filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            if len(re.findall(pattern_duokan_comment, text)) == 0:
                continue

        process_comment(file_path)
