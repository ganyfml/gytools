#!/usr/bin/env python

import json
import requests
import sys
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#bestbuy
bestbuy_url = 'http://www.bestbuy.com'
bestbuy_graphicsCardURL = 'http://www.bestbuy.com/site/searchpage.jsp?cp=page_num&_dyncharset=UTF-8&id=pcat17071&browsedCategory=pcmcat182300050008&st=categoryid%24pcmcat182300050008'

def get_url_byPageNum(baseUrl, pageNum):
    return baseUrl.replace('page_num', str(pageNum))

def get_products_byUrl(url):
    base_page_html = requests.get(get_url_byPageNum(url, 1), headers = headers)
    soup = BeautifulSoup(base_page_html.text, "html.parser")
    total_pageNum = len(soup.find('div', { 'class' : 'results-pagination'}).find_all('li')) - 2
    for page in range(1, total_pageNum + 1):
        onepage = requests.get(get_url_byPageNum(url, page), headers = headers)
        soup = BeautifulSoup(onepage.text, "html.parser")
        products = soup.find_all("div", { "class" : "list-item" })
        for product in products:
            product_body_url = bestbuy_url + product['data-url']
            product_body_html = requests.get(product_body_url, headers = headers).text
            print product['data-name'] + ' : ' + get_product_overview(product_body_html)

def get_product_overview(product_body_html):
        soup = BeautifulSoup(product_body_html, "html.parser")
        return soup.find('span', { 'class' : 'average-score' }).contents[0]

get_products_byUrl(bestbuy_graphicsCardURL)
