#!/usr/bin/env python

import requests
import string
from bs4 import BeautifulSoup
import sys
import codecs
import locale

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#GARD
URL = 'https://rarediseases.info.nih.gov/gard/browse-by-first-letter/'

def get_diseases_byUrl(url):
    disease_list_page = requests.get(url, headers = headers)
    soup = BeautifulSoup(disease_list_page.text, 'html.parser')
    diseases = soup.find_all('td', { 'class' : 'DiseaseList' })
    for d in diseases:
        disease_name = d.text.strip()
        if '- See' not in disease_name:
            print disease_name

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
reload(sys)
sys.setdefaultencoding('utf8')

disease_range = list(string.ascii_lowercase) + ['0-9']
for d in disease_range:
    get_diseases_byUrl(URL + d)
