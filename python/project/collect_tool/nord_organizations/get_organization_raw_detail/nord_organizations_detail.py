#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import requests
import sys
import re
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

html = sys.stdin.read()
soup = BeautifulSoup(html, "html.parser")
org_elements_tag = soup.find_all('div', class_ = 'po-box')
org_elements_list = []
org_elements_list.append(('name', soup.find('h3', class_ = 'po-primary-title').text))
for e in org_elements_tag:
	if e.p:
		if e.h4.text != '*Important':
			org_elements_list.append((e.h4.text, e.p.text))
	elif e.a:
		if len(e.find_all()) > 2:
			trimmed_text = re.sub('\s+', ' ', e.text.strip())
			text_title, text_content = re.match('(.*?) (.*)',trimmed_text).group(1, 2)
			org_elements_list.append((text_title, text_content))
		else:
			org_elements_list.append((e.h4.text, e.a.text))
	elif e.h4:
		org_elements_list.append((e.h4.text, e.contents[2].strip()))
org_detail = ['\002'.join([org_info_category, org_info_content]) for (org_info_category, org_info_content) in org_elements_list]
print '\t'.join(org_detail).encode('utf-8')
