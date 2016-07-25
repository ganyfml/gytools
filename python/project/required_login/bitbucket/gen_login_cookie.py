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

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
		'User-Agent': agent
		, 'Referer' : 'https://bitbucket.org/account/signin/?next=/'
		}
session = requests.Session()
session.headers.update(headers)
url = 'https://bitbucket.org/account/signin/?next=/'
session.get(url, headers = headers)

username = sys.argv[1]
password = sys.argv[2]
cookie = sys.argv[3]

postdata = {
		'csrfmiddlewaretoken' : session.cookies['csrftoken']
		, 'username' : username
		, 'password' : password
		}
post_url = 'https://bitbucket.org/account/signin/'
login_page = session.post(post_url, postdata, headers = headers)

if 'signin' in login_page.url:
	print 'login failed!'
else:
	with open(cookie, 'wb+') as f:
		json.dump(session.cookies.get_dict(), f)
