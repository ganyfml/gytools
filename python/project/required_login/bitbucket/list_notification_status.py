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

BOOL2STR = {True : 'T', False : 'F'}
def print_notification_status(repo_path, session):
	headers = {
			'X-CSRFToken' : session.cookies['csrftoken']
			, 'Referer' : 'https://bitbucket.org/account/signin/?next=/'
			, 'X-Requested-With' : 'XMLHttpRequest'
			}
	follow_status_url = os.path.join('https://bitbucket.org', repo_path, 'follow')
	session.post(url = follow_status_url, headers = headers)
	response = session.post(follow_status_url, headers = headers)
	repo_watch_status = response.json()['following']

	if repo_watch_status:
		response = session.post(
				url = os.path.join('https://bitbucket.org/xhr/watch-prefs', repo_path)
				, data = '{}'
				, headers = headers
				)
		repo_subscription_status = [BOOL2STR[response.json()[key]] for key in ['commits', 'forks', 'pullrequests']]
	else:
		repo_subscription_status = ['', '', '']
	print '\t'.join([repo_path, BOOL2STR[repo_watch_status]] + repo_subscription_status)

session = requests.Session()
with open(cookie_file, 'rb') as f:
	session.cookies.update(json.load(f))

print '\t'.join(['repo', 'watching', 'commit', 'fork', 'pullrequest'])
for repo_path in sys.stdin:
	print_notification_status(repo_path.rstrip('\n'), session)
