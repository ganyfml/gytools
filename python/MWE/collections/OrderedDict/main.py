#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from collections import OrderedDict 

d = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
print OrderedDict(sorted(d.items(), key=lambda t: t[0]))
