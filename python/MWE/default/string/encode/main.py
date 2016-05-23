#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

test = '\xce\xb1'
source_code = test.decode('utf-8')
print source_code
utf8_code = source_code.encode('utf-8')
print utf8_code
