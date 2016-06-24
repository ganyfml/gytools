#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import requests
import json
import sys
import pickle as pk

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
		'User-Agent': agent,
		'Referer' : 'https://bitbucket.org/account/signin/?next=/'
		}

def print_notification_status(url):
	post_url = 'https://bitbucket.org/xhr/watch-prefs/' + url
	header = {
			'X-CSRFToken' : session.cookies['csrftoken'],
			'Referer' : 'https://bitbucket.org/account/signin/?next=/'}
	payload = {}
	response = session.post(post_url, headers = header, data = json.dumps(payload))
	print url.split('/')[1] + '\t',
	print '\t'.join([str(response.json()[key]) for key in ['commits', 'forks', 'pullrequests']])

def set_notification_status(url, status_list):
	keys = ['commits', 'forks', 'pullrequests']
	if len(status_list) != 3:
		pass
	else:
		status_info = zip(keys, status_list)
		status_payload = {info[0] : bool(info[1]) for info in status_info}
		post_url = 'https://bitbucket.org/xhr/watch-prefs/' + url
		header = {
				'X-CSRFToken' : session.cookies['csrftoken'],
				'Referer' : 'https://bitbucket.org/account/signin/?next=/'}
		response = session.post(post_url, headers = header, data = json.dumps(status_payload))

with open(sys.argv[1], 'rb') as f:
	session = requests.Session()
	session.cookies = pk.load(f)
	print '\t'.join(['repo', 'commit', 'forks', 'pullrequests'])
	for repo in sys.stdin:
		print_notification_status(repo.rstrip('\n'))
