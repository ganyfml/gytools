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

def boolenTostr(boolvalue):
	if boolvalue:
		return 'T'
	else:
		return 'F'

def print_notification_status(repo_url, session):
	subscription_status_url = os.path.join('https://bitbucket.org/xhr/watch-prefs', repo_url)
	header = {
			'X-CSRFToken' : session.cookies['csrftoken']
			, 'Referer' : 'https://bitbucket.org/account/signin/?next=/'
			, 'X-Requested-With' : 'XMLHttpRequest'
			}
	response = session.post(subscription_status_url, headers = header, data = '{}')
	repo_subscription_status = [boolenTostr(response.json()[key]) for key in ['commits', 'forks', 'pullrequests']]

	follow_status_url = os.path.join('https://bitbucket.org/', repo_url, 'follow')
	session.post(follow_status_url, headers = header)
	response = session.post(follow_status_url, headers = header)
	repo_follow_status = boolenTostr(response.json()['following'])

	repo_name = repo_url.split('/')[1].rstrip('.git')
	repo_notification_status = [repo_name, repo_follow_status] + repo_subscription_status
	print '\t'.join(repo_notification_status)

cookie = sys.argv[1]
session = requests.Session()
with open(cookie, 'rb') as f:
	session.cookies.update(json.load(f))

print '\t'.join(['repo', 'watching', 'commit', 'forks', 'pullrequests'])
for repo in sys.stdin:
	print_notification_status(repo.rstrip('\n'), session)
