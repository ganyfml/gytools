#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from multiprocessing import Pool

def f_multi_process(args):
	return f(*args)

def f(x, y):
	return x + y

if __name__ == '__main__':
	p = Pool(5)
	args = [(1,2),(2,3)]
	print(p.map(f_multi_process, args))
