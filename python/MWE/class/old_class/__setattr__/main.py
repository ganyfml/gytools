#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

class test():
	def __init__(self, value):
		self.a = value

	def __setattr__(self, name, value):
		print "Set!"
		self.__dict__[name] = value

	def __getattribute__(self, name):
		return "Get __getattribute__"

	def __getattr__(self, name):
		return "Get __getattr__"

a = test(1)
a.c = 2
print a.a
print a.c
print a.z
