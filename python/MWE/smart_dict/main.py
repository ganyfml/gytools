#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

class smart_dict(dict):
	def __missing__(self, key):
		return 0

a = smart_dict()
print a['aaa']
