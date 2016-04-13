#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import sys
import codecs
import locale

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#NORD
URL = "http://rarediseases.org/for-patients-and-families/information-resources/rare-disease-information"

def get_num_pages(url):
    disease_list_page = requests.get(url, headers = headers)
    soup = BeautifulSoup(disease_list_page.text, "html.parser")
    page_indexs = soup.find('ul', { 'class' : 'pagination' }).find_all('li')
    return int(page_indexs[len(page_indexs) - 2].text)

def get_diseases_byUrl(url):
    disease_list_page = requests.get(url, headers = headers)
    soup = BeautifulSoup(disease_list_page.text, "html.parser")
    diseases = soup.find_all("article")
    for d in diseases:
       print d.find('a').text

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
reload(sys)
sys.setdefaultencoding('utf8')

for i in range(1, get_num_pages(URL) + 1):
    get_diseases_byUrl('%s/page/%s/' % (URL, i))
