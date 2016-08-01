#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
import signal
#http://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
signal.signal(signal.SIGINT, lambda x,y: sys.exit(128 + signal.SIGINT))

#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

import requests

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
		'User-Agent': agent
		, 'Referer' : 'https://bitbucket.org/account/signin/?next=/'
		}
session = requests.Session()
session.headers.update(headers)
session.get(url='https://bitbucket.org/account/signin/?next=/', headers=headers)

username = sys.argv[1]
password = sys.argv[2]

login_page = session.post(
		url = 'https://bitbucket.org/account/signin/'
		, data = {
			'csrfmiddlewaretoken' : session.cookies['csrftoken']
			, 'username' : username
			, 'password' : password
			}
		, headers = headers
		)

import json
import re

if 'signin' in login_page.url:
	print >> sys.stderr, re.search('data-errors=".*&#34;(.*)&#34;.*"', login_page.text).group(1)
	sys.exit(1)
else:
	print json.dumps(session.cookies.get_dict())
