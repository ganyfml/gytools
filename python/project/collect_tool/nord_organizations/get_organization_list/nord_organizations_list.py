#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#NORD
NORD_ORGANIZATIONS_URL = 'http://rarediseases.org/organizations'

def get_num_pages(url):
	disease_list_page = requests.get(url, headers = HEADERS)
	soup = BeautifulSoup(disease_list_page.text, 'html.parser')
	page_indexs = soup.find('ul', { 'class' : 'pagination' }).find_all('li')
	return int(page_indexs[len(page_indexs) - 2].text)

def print_orgAndlink_fromUrl(url):
	org_list_page = requests.get(url, headers = HEADERS)
	soup = BeautifulSoup(org_list_page.text, 'html.parser')
	orgs = soup.find_all('article')
	for o in orgs:
		o_link = (o.a)['href']
		o_name = (o.a).text.strip()
		print '\t'.join([o_name, o_link]).encode('utf-8')

for i in range(get_num_pages(NORD_ORGANIZATIONS_URL)):
	print_orgAndlink_fromUrl('%s/page/%s/' % (NORD_ORGANIZATIONS_URL, i+1))
