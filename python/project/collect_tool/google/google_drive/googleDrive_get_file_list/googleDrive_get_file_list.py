#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
import signal
#http://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
signal.signal(signal.SIGINT, lambda x,y: sys.exit(128 + signal.SIGINT))

#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from collections import defaultdict

credential_path = sys.argv[1]
credentials = oauth2client.file.Storage(credential_path).get()
service = build('drive', 'v3', http=credentials.authorize(Http()))

def get_all_items(folder_dict, file_dict):
	items = service.files().list(pageSize = 1000, fields = "files(name, webViewLink, mimeType, id, parents)").execute().get('files', [])
	for item in items:
		if('folder' in item['mimeType']):
			if 'parents' not in item:
				folder_dict[item['id'].encode('utf-8')].append((item['name'].encode('utf-8'), 'root'))
			else:
				folder_dict[item['id'].encode('utf-8')].append((item['name'].encode('utf-8'), item['parents'][0].encode('utf-8')))
		else:
			if 'parents' not in item:
				file_dict['root'].append([item['name'].encode('utf-8'), item['webViewLink'].encode('utf-8')])
			else:
				file_dict[item['parents'][0].encode('utf-8')].append([item['name'].encode('utf-8'), item['webViewLink'].encode('utf-8')])

def get_file_path(parent_id, folder_dict):
	path = ""
	while parent_id in folder_dict:
		path = '/'.join([folder_dict[parent_id][0][0], path])
		parent_id = folder_dict[parent_id][0][1]
	return path

folder_dict = defaultdict(list)
file_dict = defaultdict(list)
get_all_items(folder_dict, file_dict)

for parent_id, files_info in file_dict.iteritems():
	for file_info in files_info:
		print '\t'.join([get_file_path(parent_id, folder_dict) + file_info[0], file_info[1]])
