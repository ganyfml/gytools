#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

class test(object):
	def __setattr__(self, name, value):
		print 'set'
		object.__setattr__(self, name, value)

a = test()
a.c = 2
print a.c
print a.a
