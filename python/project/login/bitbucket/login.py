#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import requests
import sys
import pickle as pk

with open(sys.argv[1], 'wb+') as f:
	agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
	headers = {
			'User-Agent': agent,
			'Referer' : 'https://bitbucket.org/account/signin/?next=/'
			}
	session = requests.Session()
	session.headers.update(headers)
	url = 'https://bitbucket.org/account/signin/?next=/'
	session.get(url, headers = headers)
	post_url = 'https://bitbucket.org/account/signin/'
	username = raw_input("user name:>")
	password = raw_input("password:>")
	postdata = {
			'csrfmiddlewaretoken': session.cookies['csrftoken'],
			'username' : username,
			'password' : password
			}
	login_page = session.post(post_url, postdata, headers = headers)
	if 'signin' in login_page.url:
		print 'login failed!'
	else:
		pk.dump(session.cookies, f, True)
