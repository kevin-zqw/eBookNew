#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals, division, absolute_import, print_function
import sys
import re

def run(bk):
	lastid = 0
	fnid = 0
	fnid1 = 0

	note_sup = r'\[\[(.*?):(.*?)\]\]'
	note_p = r'\<p\>\[\[(.*?):(.*?)\]\](.+)\<\/p\>\n'
# all xhtml/html files - moves found notes to end of file, insert a link in the text and link to css in the files with notes
	for (id, href) in bk.text_iter():
		html = bk.readfile(id)
		html_original = html
		found = re.search(note_sup,html)
		found1 = re.search(note_p,html)
		if found is not None: #only once for each file with notes
			html = re.sub(r'\<\/body\>',r'<div>\n<hr class="xian"/>\n</div>\n<ol class="duokan-footnote-content">\n</ol>\n</body>',html)
		while found1 is not None:
			fnid1 = fnid1+1
			html = re.sub(note_p,r'',html,1)
			html = re.sub(r'\<\/ol\>',r'\n<li class="duokan-footnote-item" id="B_'+found1.group(1)+r'">\n<p class="footnote"><a style="text-decoration:none!important;color:black;" href="#A_'+found1.group(2)+r'">◎</a>'+found1.group(3)+r'&#8203;​​​​​​​​</p>\n</li>\n</ol>',html,1)
			print(id, href, 'id:'+found1.group(1).strip('[]^')+'; href:'+found1.group(2).strip('[]^')+'; footnote:'+found1.group(3))
			found1 = re.search(note_p,html)
		while found is not None:
			fnid = fnid+1
			html = re.sub(note_sup,r'<sup><a style="text-decoration:none!important;color:black;" class="duokan-footnote" href="#B_\2" id="A_\1"><img alt="" src="../Images/note.png"/></a></sup>',html,1)
			print(id, href, 'id:'+found.group(1).strip('[]^')+'; href:'+found.group(2).strip('[]^'))
			found = re.search(note_sup,html)
		else:
			print(id, href, "No notes found")
		if not html == html_original:
			bk.writefile(id,html)
		lastid = id
#css
	if fnid > 0:
		cssdata = '/*多看注释*/\nsup img{\n    width:0.96em;\n    height:0.96em;\n    margin:0;\n    padding-top:0.5em;\n    vertical-align: text-top;\n}'
		cssdata = cssdata + '\n/*分割线*/\nhr.xian{\n    text-align: left;\n    duokan-text-align: left;\n    width: 60%;\n    height: 1px;\n    margin: 1.5em 0 1.5em -0.5em;\n    border-style: none;\n    border-top: 1px solid gray;\n}'
		cssdata = cssdata + '\nol{\n    padding: 0;\n    list-style-type: none;\n    list-style-position: outside;\n}'
		cssdata = cssdata + '\n/*注释框架*/\n.duokan-footnote-content{\n    text-align: justify;\n    margin-left: 1em;\n}'
		cssdata = cssdata + '\n/*注释内容*/\n.footnote{\n    font-size: 0.92em;\n    line-height: 1.6;\n    font-family: "fs";\n    margin: 0 0 0 0em;\n    text-indent: -1em;\n}'
		cssdata = cssdata + '\n/*链接颜色*/\na{color: black}'
		basename = "footnote.css"
		uid = "footnotecss"
		mime = "text/css"
		bk.addfile(uid, basename, cssdata, mime)
	return 0

def main():
	print("I reached main when I should not have\n")
	return -1

if __name__ == "__main__":
	sys.exit(main())
