#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

def foo(*args):
	for a in args:
		print a

foo(1,2,3)
