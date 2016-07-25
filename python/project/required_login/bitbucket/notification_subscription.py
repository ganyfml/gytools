#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
import signal
#http://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
signal.signal(signal.SIGINT, lambda x,y: sys.exit(128 + signal.SIGINT))

#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

import requests
import json
import os

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
		'User-Agent': agent,
		'Referer' : 'https://bitbucket.org/account/signin/?next=/'
		}

def set_notification_status(repo_url, status_list):
	if len(status_list) != 4:
		print "ERROR: requrie 4 status!"
		pass
	else:
		header = {
				'X-CSRFToken' : session.cookies['csrftoken']
				, 'Referer' : 'https://bitbucket.org/account/signin/?next=/'
				, 'X-Requested-With' : 'XMLHttpRequest'
				}
		keys = ['commits', 'forks', 'pullrequests']
		subscription_payload = dict(zip(keys, status_list[1:]))
		subscription_url = os.path.join('https://bitbucket.org/xhr/watch-prefs', repo_url)
		response = session.post(subscription_url, headers = header, data = json.dumps(subscription_payload))
		
		follow_url = os.path.join('https://bitbucket.org/', repo_url, 'follow')
		if session.post(follow_url, headers = header).json()['following'] != status_list[0]:
			response = session.post(follow_url, headers = header)

cookie = sys.argv[1]
status = [bool(int(s)) for s in sys.argv[2:]]

session = requests.Session()
with open(cookie, 'rb') as f:
	session.cookies.update(json.load(f))

for repo_url in sys.stdin:
	set_notification_status(repo_url.rstrip('\n'), status)
