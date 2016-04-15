#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#NORD
NORD_URL = "http://rarediseases.org/for-patients-and-families/information-resources/rare-disease-information"

def get_num_pages(url):
	disease_list_page = requests.get(url, headers = HEADERS)
	soup = BeautifulSoup(disease_list_page.text, "html.parser")
	page_indexs = soup.find('ul', { 'class' : 'pagination' }).find_all('li')
	return int(page_indexs[len(page_indexs) - 2].text)

def print_diseases_fromUrl(url):
	disease_list_page = requests.get(url, headers = HEADERS)
	soup = BeautifulSoup(disease_list_page.text, "html.parser")
	diseases = soup.find_all("article")
	for d in diseases:
		print d.find('a').text.encode('utf-8')

for i in range(get_num_pages(NORD_URL)):
	print_diseases_fromUrl('%s/page/%s/' % (NORD_URL, i+1))
