#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import requests
import string
from bs4 import BeautifulSoup
import os

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def print_diseases_fromUrl(url):
	disease_list_page = requests.get(url, headers = HEADERS)
	soup = BeautifulSoup(disease_list_page.text, 'html.parser')
	diseases = soup.find_all('td', { 'class' : 'DiseaseList' })
	for d in diseases:
		disease_name = d.text.strip()
		if '- See' not in disease_name:
			print disease_name.encode('utf-8')

#GARD
url = 'https://rarediseases.info.nih.gov/gard/browse-by-first-letter'
disease_pages = list(string.ascii_lowercase) + ['0-9']
for p in disease_pages:
	print_diseases_fromUrl(os.path.join(url, p))
