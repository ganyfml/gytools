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

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
		'User-Agent': agent,
		'Referer' : 'https://bitbucket.org/account/signin/?next=/'
		}

STRING2BOOL = {'T' : True, 'F' : False}
def set_notification_status(repo_path, status_list):
	(watch_status, commit_status, fork_status, pullrequest_status) = status_list
	headers = {
			'X-CSRFToken' : session.cookies['csrftoken']
			, 'Referer' : 'https://bitbucket.org/account/signin/?next=/'
			, 'X-Requested-With' : 'XMLHttpRequest'
			}
	response = session.post(
			url = os.path.join('https://bitbucket.org/xhr/watch-prefs', repo_path)
			, data = json.dumps({'commits': commit_status, 'forks': fork_status, 'pullrequests': pullrequest_status})
			, headers = headers
			)

	follow_url = os.path.join('https://bitbucket.org', repo_path, 'follow')
	if session.post(url=follow_url, headers=headers).json()['following'] != watch_status:
		response = session.post(url=follow_url, headers=headers)

status = [STRING2BOOL[s] for s in sys.argv[2:]]

session = requests.Session()
with open(cookie_file, 'rb') as f:
	session.cookies.update(json.load(f))

for repo_path in sys.stdin:
	set_notification_status(repo_path.rstrip('\n'), status)
