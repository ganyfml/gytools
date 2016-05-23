#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from functools import partial

def power(base, exponent):
	return base ** exponent

square = partial(power, exponent=2)
#def square(base):
#	return power(base, 2)

cube = partial(power, exponent=3)
#def cube(base):
#	return power(base, 3)
