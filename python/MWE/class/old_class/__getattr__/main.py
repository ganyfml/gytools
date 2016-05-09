#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

class test:
	def __getattr__(self, attr):
		print "Get here with attr: " + attr

a = test()
a.bbb
