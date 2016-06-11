#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import track_repository
from selenium import webdriver

browser = webdriver.PhantomJS()
track_repository.login(browser)
result = {}
track_repository.check_repo_notification(browser, '/ehsanr/nlpxplat', result)
print result
browser.quit()
