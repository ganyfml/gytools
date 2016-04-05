#!/usr/bin/env python

import sqlite3
import random
import ast
import json
import requests
import sys
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#bestbuy
amazon_url = 'http://www.amazon.com/s/ref=lp_284822_pg_2?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A193870011%2Cn%3A284822&page=page_num'

def get_url_byPageNum(baseUrl, pageNum):
    return baseUrl.replace('page_num', str(pageNum))

def get_product_title(soup):
    return soup.find('span', { 'id' : 'productTitle' }).text.replace('"', "'")

def get_product_price(soup):
    return soup.find('span', { 'id' : 'priceblock_ourprice' }).text.replace("$","")

def get_product_rate(soup):
    return float(soup.find('div', { 'id' : 'averageCustomerReviews' }).find('span', { 'class' : 'a-icon-alt'}).text.split(' ')[0])

def get_product_numReview(soup):
    return int(soup.find('span', { 'id' : 'acrCustomerReviewText' }).text.split(' ')[0].replace(',', ''))

def get_product_image(soup):
    return ast.literal_eval(soup.find('img', { 'id' : 'landingImage'})['data-a-dynamic-image']).keys()[0]

def get_review_url(soup):
    return soup.find('div', { 'id' : 'customer-reviews_feature_div' }).find('div', { 'id' : 'revF' }).find('a')['href'] + '&pageNumber=page_num&reviewerType=avp_only_reviews'

def get_reviews(soup):
    table = soup.find('table', { 'id' : 'productDetails_techSpec_section_2' })
    model = 'NA'
    rows = table.findChildren(['tr'])
    ret = []
    for row in rows:
        if row.find('th').text.strip() == "Item model number":
            model = '"' + row.find('td').text.strip() + '"'

    review_soup = BeautifulSoup(requests.get(get_review_url(soup), headers = headers).text, "html.parser")
    reviews = review_soup.find_all('div', { 'class' : 'a-section review' })
    for review in reviews:
        list_current_review = []
        user_name = '"' + review.find('span', { 'class' : 'a-size-base review-text'}).text.replace('"',"'") + '"'
        content = '"' + review.find('a', { 'class' : 'a-size-base a-link-normal author'}).text.replace('"', "'") + '"'
        list_current_review.append(model)
        list_current_review.append(user_name)
        list_current_review.append(content)
        ret.append(list_current_review)
    return ret

def get_technical_info(soup):
    annotation = {'Processor' : 'p_speed', 'Memory Speed' : 'm_speed'
            , 'Chipset Brand' : 'chip_brand', 'Graphics Card Ram Size' : 'memory'
            , 'Item model number' : 'model', 'Brand Name' : 'brand'}
    ret = {}
    table = soup.find('table', { 'id' : 'productDetails_techSpec_section_1' })
    rows = table.findChildren(['tr'])
    for row in rows:
	try:
	    ret[annotation[row.find('th').text.strip()]] = row.find('td').text.strip().upper()
	except:
	    pass

    table = soup.find('table', { 'id' : 'productDetails_techSpec_section_2' })
    rows = table.findChildren(['tr'])
    for row in rows:
	try:
	    ret[annotation[row.find('th').text.strip()]] = row.find('td').text.strip()
	except:
	    pass
    return ret

def get_card_info(soup):
    ret = {}
    ret['title'] = get_product_title(soup)
    ret['price_amazon'] = get_product_price(soup)
    ret['price_bestbuy'] = str(float(ret['price_amazon']) + float('%.1f' % random.uniform(0, 15)))
    ret['price_newegg'] = str(float(ret['price_amazon']) + float('%.1f' % random.uniform(0, 15)))
    ret['image'] = get_product_image(soup)
    ret['rate'] = get_product_rate(soup)
    ret['num_reviews'] = get_product_numReview(soup)
    tech = get_technical_info(soup)
    ret.update(tech)
    return ret

def write_card_info_to_db(db, soup):
    data = get_card_info(soup)
    print data
    time = '"2016-03-08 21:18:52.558836"'
    attr = ','.join(data.keys())
    attr += ", created_at, updated_at"
    value = ','.join(str(data[key]) if type(data[key]) == int or type(data[key]) == float else str('"' + data[key] + '"') for key in data.keys())
    value += ',' + time + ',' + time
    command = 'INSERT INTO PRODUCTS (' + attr + ') VALUES(' + value + ')'
    try:
        db.execute(command)
        db.commit()
    except:
        print command

def get_products_specs(url):
    base_page_html = requests.get(get_url_byPageNum(url, 1), headers = headers)
    soup = BeautifulSoup(base_page_html.text, "html.parser")
    db = sqlite3.connect('development.sqlite3')
    for page in range(1, 5):
	onepage = requests.get(get_url_byPageNum(url, page), headers = headers)
	soup = BeautifulSoup(onepage.text, "html.parser")
	products = soup.find_all("li", { "class" : "s-result-item  celwidget " })
	for product in products:
	    product_soup = BeautifulSoup(requests.get(product.find('a', { 'class' : 'a-link-normal a-text-normal'})['href'], headers = headers).text, "html.parser")
	    try:
		write_card_info_to_db(db, product_soup)
	    except:
		print product.find('a', { 'class' : 'a-link-normal a-text-normal'})['href']

def write_card_review_info_to_db(db, soup):
    reviews = get_reviews(soup)
    time = '"2016-03-08 21:18:52.558836"'
    attr = "model, content, user_name, created_at, updated_at"
    for review in reviews:
        value = ','.join(review)
        value += ',' + time + ',' + time
        command = 'INSERT INTO REVIEWS (' + attr + ') VALUES(' + value + ')'
        try:
            db.execute(command)
            db.commit()
        except:
            print command

def get_products(url):
    base_page_html = requests.get(get_url_byPageNum(url, 1), headers = headers)
    soup = BeautifulSoup(base_page_html.text, "html.parser")
    db = sqlite3.connect('development.sqlite3')
    for page in range(1, 5):
        onepage = requests.get(get_url_byPageNum(url, page), headers = headers)
        soup = BeautifulSoup(onepage.text, "html.parser")
        products = soup.find_all("li", { "class" : "s-result-item  celwidget " })
        for product in products:
            try:
                product_soup = BeautifulSoup(requests.get(product.find('a', { 'class' : 'a-link-normal a-text-normal'})['href'], headers = headers).text, "html.parser")
                write_card_review_info_to_db(db, product_soup)
                write_card_info_to_db(db, product_soup)
            except:
                print "PASS"
                pass

get_products(amazon_url)
