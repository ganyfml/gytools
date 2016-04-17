#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

def foo(a, b):
	print a, b

a = [1, 2]
b = {1, 2}
c = (1, 2)

foo(*a)
foo(*b)
foo(*c)
