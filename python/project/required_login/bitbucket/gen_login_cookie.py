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

username = sys.argv[1]
password = sys.argv[2]

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
		'User-Agent': agent
		, 'Referer' : 'https://bitbucket.org/account/signin/?next=/'
		}
session = requests.Session()
session.headers.update(headers)
session.get(url='https://bitbucket.org/account/signin/?next=/', headers=headers)

login_page = session.post(
		url = 'https://bitbucket.org/account/signin/'
		, data = {
			'csrfmiddlewaretoken' : session.cookies['csrftoken']
			, 'username' : username
			, 'password' : password
			}
		, headers = headers
		)

if 'signin' in login_page.url:
	print 'login failed!'
else:
	print json.dumps(session.cookies.get_dict())
