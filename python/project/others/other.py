#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

#Used for Ctrl-C
import signal
import sys
#http://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
signal.signal(signal.SIGINT, lambda x,y: sys.exit(128 + signal.SIGINT))

#Used for pip
#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

import requests
import urllib
from bs4 import BeautifulSoup
import time
import os
from multiprocessing import Pool as ThreadPool 

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
MAINPAGE_URL = 'http://t66y.com/thread0806.php?fid=16&search=&page='
BASE_URL = 'http://t66y.com'

def write_image_toFile(url, path):
	try:
		r = requests.get(url, stream=True)
		if r.status_code == 200:
			with open(path, 'wb') as f:
				for chunk in r:
					f.write(chunk)
	except requests.exceptions.RequestException as e:
		print e

def save_images_fromThread_multi_wrapper(args):
	return save_images_fromThread(*args)

def save_images_fromThread(url, thread_save_path, thread_num):
	thread_soup = BeautifulSoup(requests.get(url, headers = HEADERS).text, "lxml")
	imgs = thread_soup.find('div', { 'class' : 'tpc_content do_not_catch' })
	img_id = 0
	for i in imgs.find_all('input'):
		img_url = i['src']
		if 'sinaimg' not in img_url:
			img_format = 'jpg'
			if(len(img_url.split('.')[-1]) < 5):
					img_format = img_url.split('.')[-1]
			img_name = '.'.join([str(thread_num) + '-' + str(img_id), img_format])
			write_image_toFile(img_url, os.path.join(thread_save_path, img_name))
			img_id += 1
	print "Thread " + str(thread_num) + " finished!"

def vaild_threadTag(tag):
	target_valid = tag.has_attr('target') and tag['target'] == '_blank'
	title_valid = tag.has_attr('title')
	href_valid = tag.has_attr('href') and 'htm_data' in tag['href']
	return (target_valid and title_valid and href_valid)

def cache_page(page_index):
	main_page = BeautifulSoup(requests.get(MAINPAGE_URL + str(page_index), headers = HEADERS).text, "lxml")
	folder = os.path.join('/tmp', time.asctime())
	os.mkdir(folder)
	thread_num = 0
	thread_argvs = []
	for p in main_page.find_all(vaild_threadTag):
		thread_argvs.append((os.path.join(BASE_URL, p['href']), folder, thread_num))
		thread_num += 1
	pool = ThreadPool(20)
	pool.map(save_images_fromThread_multi_wrapper,thread_argvs)

cache_page(1)
