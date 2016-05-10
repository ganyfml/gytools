#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import multiprocessing
import time

def func(x):
	time.sleep(x)
	return x + 2

if __name__ == "__main__":    
	p = multiprocessing.Pool()
	start = time.time()
	for x in p.imap_unordered(func, [1,5,3]):
		print("{} (Time elapsed: {}s)".format(x, int(time.time() - start)))
