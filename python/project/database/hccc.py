#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from pymongo import MongoClient

client = MongoClient('128.194.140.206', 27017)

db = client.tti
log_db = client.log

