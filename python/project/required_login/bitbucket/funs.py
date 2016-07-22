#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import requests
import json
import os
import sys
import pickle as pk

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
		'User-Agent': agent,
		'Referer' : 'https://bitbucket.org/account/signin/?next=/'
		}

def print_notification_status(repo_url, session):
	subscription_status_url = os.path.join('https://bitbucket.org/xhr/watch-prefs', repo_url)
	header = {
			'X-CSRFToken' : session.cookies['csrftoken']
			, 'Referer' : 'https://bitbucket.org/account/signin/?next=/'
			, 'X-Requested-With' : 'XMLHttpRequest'
			}
	response = session.post(subscription_status_url, headers = header, data = '{}')
	repo_subscription_status = [str(response.json()[key]) for key in ['commits', 'forks', 'pullrequests']]

	follow_status_url = os.path.join('https://bitbucket.org/', repo_url, 'follow')
	session.post(follow_status_url, headers = header, allow_redirects = False)
	response = session.post(follow_status_url, headers = header, data = '')
	repo_follow_status = str(response.json()['following'])

	repo_name = repo_url.split('/')[1]
	repo_notification_status = [repo_name] + [repo_follow_status] + repo_subscription_status
	print '\t'.join(repo_notification_status)

#def set_notification_status(repo_url, status_list):
#	keys = ['commits', 'forks', 'pullrequests']
#	if len(status_list) != 3:
#		pass
#	else:
#		status_payload = dict(zip(keys, status_list))
#		post_url = os.path.join('https://bitbucket.org/xhr/watch-prefs', repo_url)
#		header = {
#				'X-CSRFToken' : session.cookies['csrftoken'],
#				'Referer' : 'https://bitbucket.org/account/signin/?next=/'}
#		response = session.post(post_url, headers = header, data = json.dumps(status_payload))

session = requests.Session()
with open(sys.argv[1], 'rb') as f:
	session.cookies = pk.load(f)
print '\t'.join(['repo', 'follow', 'commit', 'forks', 'pullrequests'])
for repo in sys.stdin:
	print_notification_status(repo.rstrip('\n'), session)
