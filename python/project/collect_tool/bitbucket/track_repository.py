#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import getpass
import json

def login(browser):
	browser.get('https://bitbucket.org/account/signin/?next=/')
	email_box = browser.find_element_by_xpath('//*[@id="js-email-field"]')
	email_address = raw_input('Email:>')
	email_box.send_keys(email_address.strip())
	password_box = browser.find_element_by_xpath('//*[@id="js-password-field"]')
	password = getpass.getpass('Password:>')
	password_box.send_keys(password.strip())
	browser.find_element_by_xpath('//*[@id="aid-login-form"]/div[2]/input').click()

def check_repo_watched(browser, url):
	base_URL = 'https://bitbucket.org/'
	browser.get(base_URL + url + '/overview')
	try:
		watch_element =  browser.find_element_by_xpath('//*[@id="repo-content"]/div[1]/div[2]/div[4]/a[1]')
		return 'Stop' in watch_element.get_attribute('title')
	except:
		browser.save_screenshot('screen_shot.png')
		return 'Unknown'

def watch_repo(browser, url):
	base_URL = 'https://bitbucket.org/'
	browser.get(base_URL + url)
	WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="repo-content"]/div[2]/div[2]/div[4]/a[1]')))
	browser.find_element_by_xpath('//*[@id="repo-content"]/div[2]/div[2]/div[4]/a[1]').click()

def check_repo_notification(browser, url, result):
	base_URL = 'https://bitbucket.org/xhr/watch-prefs'
	browser.get(base_URL + url)
	result.update(json.loads(browser.find_element_by_tag_name('body').text))

def select_repo_notification(browser, url, notify_choice):
	base_URL = 'https://bitbucket.org'
	browser.get(base_URL + url + '/overview')
	WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="repo-content"]/div[1]/div[2]/div[4]/a[2]')))
	browser.find_element_by_xpath('//*[@id="repo-content"]/div[1]/div[2]/div[4]/a[2]').click()
	print "Get here"
	if 'pull requests' in notify_choice:
		browser.find_element_by_xpath('//*[@for="pref-pullrequests"]').click()
		print "Get here"
	if 'commits' in notify_choice:
		browser.find_element_by_xpath('//*[@id="pref-commits"]').click()
		print "Get here"
	if 'forks' in notify_choice:
		browser.find_element_by_xpath('//*[@id="pref-forks"]').click()
		print "Get here"

def get_all_repo_status(browser, repos_info):
	repo_dict = {}
	get_all_repos(browser, repo_dict)
	for repo_name, repo_address in repo_dict.items():
		watch_status = check_repo_watched(browser, repo_address)
		repo_notification = {}
		check_repo_notification(browser, repo_address, repo_notification)
		repo_notification.update({'watch' : watch_status, 'address' : repo_address})
		repos_info[repo_name] = repo_notification

def print_repo_status(repo_infos):
	print '\t'.join(['Repo Name', 'Repo Address', 'Has watched?', 'Sub for pull requests?', 'Sub for commits?', 'Sub for forks?'])
	for repo_name, repo_info in repo_infos.items():
		print '\t'.join([repo_name, repo_info['address'], str(repo_info.get('watch', 'None')), str(repo_info.get('pullrequests', 'None')), str(repo_info.get('commits', 'None')), str(repo_info.get('forks', 'None'))])

#browser = webdriver.PhantomJS()
#try:
#	login(browser)
#	print check_repo_watched(browser, '/ehsanr/nlpxplat')
#except:
#	browser.save_screenshot('screen_shot.png')
#finally:
#	browser.quit()
