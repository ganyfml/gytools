#!/usr/bin/env python

import json
import requests
import sys
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#bestbuy
bestbuy_url = 'http://www.bestbuy.com/site/searchpage.jsp?cp=page_num&_dyncharset=UTF-8&id=pcat17071&browsedCategory=pcmcat182300050008&st=categoryid%24pcmcat182300050008'

def get_url_byPageNum(baseUrl, pageNum):
    return baseUrl.replace('page_num', str(pageNum))

def get_products_byUrl(url):
    result = requests.get(get_url_byPageNum(url, 1), headers = headers)
    soup = BeautifulSoup(result.text, "html.parser")
    total_pageNum = soup.find('div', { 'class' : 'results-pagination'})
    print total_pageNum
    #products = soup.find_all("div", { "class" : "list-item" })
    #for product in products:
    #    print product['data-name']

get_products_byUrl(bestbuy_url)
