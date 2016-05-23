#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

class A(object):
	def __init__(self, value):
		self.v = value
	def __getattr__(self, name):
		return "Actually, I do not have '%s'" %name

a = A(42)
print a.v
print a.z
