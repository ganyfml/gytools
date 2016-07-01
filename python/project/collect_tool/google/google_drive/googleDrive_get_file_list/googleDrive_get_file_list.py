#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import oauth2client
import sys
from apiclient.discovery import build
from httplib2 import Http
from collections import defaultdict

tokencache = sys.argv[1]
token = oauth2client.file.Storage(tokencache).get()
service = build('drive', 'v3', http=token.authorize(Http()))

def get_all_folder_files():
	page_token = None
	items = []
	while True:
		files = service.files().list(
				pageSize = 1000
				, pageToken = page_token
				, fields = "files(name, webViewLink, mimeType, id, parents), nextPageToken"
				).execute()
		page_token = files.get('nextPageToken')
		items.extend(files['files'])
		if not page_token:
			break

	folders_dict = defaultdict(list)
	files_dict = defaultdict(list)
	for item in items:
		item_type = item['mimeType']
		item_parent_id= 'root' if 'parents' not in item else item['parents'][0]
		if('folder' in item_type):
			folder_id = item['id']
			folder_name = item['name']
			folders_dict[folder_id] = ([folder_name, item_parent_id])
		else:
			file_name = item['name']
			file_url = item['webViewLink']
			files_dict[item_parent_id].append([file_name, file_url])
	
	return folder_name, files_dict

def get_file_path(parent_id, folders_dict):
	path = ""
	while parent_id in folders_dict:
		path = '%s/%s' % (folders_dict[parent_id][0], path)
		parent_id = folders_dict[parent_id][1]
	return path

folders_dict, files_dict = get_all_folder_files()
for parent_id, files_info in files_dict.iteritems():
	parent_folder_path = get_file_path(parent_id, folders_dict)
	for file_info in files_info:
		file_path = (parent_folder_path + file_info[0]).encode('utf-8')
		file_url = file_info[1].encode('utf-8')
		print '%s\t%s' %(file_path, file_url)
