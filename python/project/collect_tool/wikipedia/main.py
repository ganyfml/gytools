#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import wikipedia
from bs4 import BeautifulSoup
import requests

term = 'Blood–brain_barrier'
page = wikipedia.page("Blood–brain barrier")
links = page.links

for l in links:
	print l.encode('utf-8')

#s = BeautifulSoup(requests.get(page.url).text, 'lxml')
#body = s.find('div', {'id': 'mw-content-text'})
#
#def a_has_href(tag):
#	return tag.name == 'a' and tag.has_attr('href')
#
#for i in body.find_all(a_has_href):
#	aa = i['href'].split('/')[-1].replace('_', ' ')
#	if aa in links:
#		print aa + '\t' + i.text
#
