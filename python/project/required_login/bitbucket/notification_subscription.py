#!/usr/bin/env python
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

cookie_file = sys.argv[1]
status = sys.argv[2:]

STRING2BOOL = {'T' : True, 'F' : False}
def set_notification_status(repo_path, status_list):
	headers = {
			'X-CSRFToken' : session.cookies['csrftoken']
			, 'Referer' : 'https://bitbucket.org/account/signin/?next=/'
			, 'X-Requested-With' : 'XMLHttpRequest'
			}
	watch_status = status_list[0]
	if watch_status != 'U':
		watch_url = os.path.join('https://bitbucket.org', repo_path, 'follow')
		if session.post(url = watch_url, headers = headers).json()['following'] != STRING2BOOL[watch_status]:
			response = session.post(url = watch_url, headers = headers)

	repo_sub_name = ['commits', 'forks', 'pullrequests']
	repo_sub_status = [status_list[status] for status in range(1, 4)]
	repo_sub_params = {name : STRING2BOOL[status] for name, status in zip(repo_sub_name, repo_sub_status) if status != 'U'}
	response = session.post(
			url = os.path.join('https://bitbucket.org/xhr/watch-prefs', repo_path)
			, data = json.dumps(repo_sub_params)
			, headers = headers
			)

session = requests.Session()
with open(cookie_file, 'rb') as f:
	session.cookies.update(json.load(f))

for repo_path in sys.stdin:
	set_notification_status(repo_path.rstrip('\n'), status)
