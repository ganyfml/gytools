#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

test = {'key1':'val1', 'key2':'val2'}

for k, v in test.iteritems():
	print "\t".join([k, v])
