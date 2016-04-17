#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

def bar(**kwargs):
	for a in kwargs:
		print a, kwargs[a]

bar(first = 'f', age = 27)
