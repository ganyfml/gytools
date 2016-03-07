#!/usr/bin/env python

import json
import requests
import sys
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#bestbuy
amazon_url = 'http://www.amazon.com/s/ref=lp_284822_pg_2?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A193870011%2Cn%3A284822&page=page_num'

def get_url_byPageNum(baseUrl, pageNum):
    return baseUrl.replace('page_num', str(pageNum))

def get_products_byUrl(url):
    base_page_html = requests.get(get_url_byPageNum(url, 1), headers = headers)
    soup = BeautifulSoup(base_page_html.text, "html.parser")
    for page in range(1, 2):
        onepage = requests.get(get_url_byPageNum(url, page), headers = headers)
        soup = BeautifulSoup(onepage.text, "html.parser")
        products = soup.find_all("li", { "class" : "s-result-item  celwidget " })
        try:
            for product in products:
                product_soup = BeautifulSoup(requests.get(product.find('a', { 'class' : 'a-link-normal a-text-normal'})['href'], headers = headers).text, "html.parser")
                title = get_product_title(product_soup)
                price = get_product_price(product_soup)
                print title + ', ' + price
        except:
            pass

def get_product_title(soup):
    return soup.find('span', { 'id' : 'productTitle' }).text

def get_product_price(soup):
    return soup.find('span', { 'id' : 'priceblock_ourprice' }).text

get_products_byUrl(amazon_url)
