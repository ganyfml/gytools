#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import requests

def login():
	login_data = {'log':'vm06', 'pwd':'vm06', 'redirect_to':'http://vmus.co/wp-admin/', 'rememberme':'forever', 'testcookie':'1', 'wp-submit':'登入'}
	login_url = 'http://vmus.co/wp-login.php'
	s = requests.session();
	s.post(login_url, login_data);
	return s
