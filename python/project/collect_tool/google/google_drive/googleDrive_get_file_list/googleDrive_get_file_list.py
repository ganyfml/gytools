#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1:

import sys
import signal
#http://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
signal.signal(signal.SIGINT, lambda x,y: sys.exit(128 + signal.SIGINT))

#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

from apiclient.discovery import build
from httplib2 import Http
import oauth2client

credential_path = sys.argv[1]
credentials = oauth2client.file.Storage(credential_path).get()
service = build('drive', 'v3', http=credentials.authorize(Http()))

exit_status=1

results = service.files().list(pageSize = 1000,fields="nextPageToken, files(name, webViewLink, mimeType)").execute()
items = results.get('files', [])

def prRed(prt):
	print("\033[91m {}\033[00m" .format(prt))

if not items:
	print('No files found.')
else:
	print('Files:')
	for item in items:
		if('folder' in item['mimeType']):
			prRed('\t'.join([item['name'].encode('utf-8'), item['webViewLink'].encode('utf-8')]))
		else:
			print('\t'.join([item['name'].encode('utf-8'), item['webViewLink'].encode('utf-8')]))
