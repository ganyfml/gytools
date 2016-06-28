#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from apiclient.discovery import build
from httplib2 import Http
import oauth2client
import webbrowser
import sys

credential_path = '/Users/gany/bin/gytools/google_drive/credential.json'
credentials = oauth2client.file.Storage(credential_path).get()
service = build('drive', 'v3', http=credentials.authorize(Http()))

page_token = None
items = []
while True:
	files = service.files().list(pageSize = 1000, fields = "files(name, webViewLink), nextPageToken", pageToken = page_token).execute()
	items.extend(files['files'])
	page_token = files.get('nextPageToken')
	if not page_token:
		break
search_result = [item for item in items if sys.argv[1].lower() in item['name'].lower()]

if len(search_result) == 0:
	print "No match record found!"
elif len(search_result) == 1:
	webbrowser.open_new(search_result[0]['webViewLink'])
else:
	for i, item in enumerate(search_result):
		print ' '.join([str(i), item['name']])
	index = raw_input('index:> ')
	webbrowser.open_new(search_result[int(index)]['webViewLink'])
