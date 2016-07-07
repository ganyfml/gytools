#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

browser = webdriver.PhantomJS()
browser.get('http://www.nsf.gov/awardsearch/advancedSearchResult?BooleanElement=All&BooleanRef=All&Program=CAREER:+FACULTY+EARLY+CAR+DEV&OriginalAwardDateOperator=After&OriginalAwardDateFrom=01/01/2016')
try:
	element = WebDriverWait(browser, 30).until(
			EC.visibility_of_element_located((By.XPATH, '//*[@id="x-auto-32"]/a'))
			)
	cookie = {'JSESSIONID' : cookie['value'] for cookie in browser.get_cookies() if cookie['name'] == 'JSESSIONID'}
	print requests.get('http://www.nsf.gov/awardsearch/ExportResultServlet?exportType=csv', cookies = cookie ).text.encode('utf-8')

finally:
	browser.quit()
