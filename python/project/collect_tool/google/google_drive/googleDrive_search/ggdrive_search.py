#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from apiclient.discovery import build
from httplib2 import Http
import oauth2client
import webbrowser
import sys
import json

program_path = '/Users/gany/bin/gytools/google_drive/'
credential_path = program_path + 'credential.json'
credentials = oauth2client.file.Storage(credential_path).get()
service = build('drive', 'v3', http=credentials.authorize(Http()))

items = service.files().list(pageSize = 1000, fields = "files(name, webViewLink)").execute().get('files', [])
def update_googleDriveData():
	items = service.files().list(pageSize = 1000, fields = "files(name, webViewLink)").execute().get('files', [])
	with open(program_path + 'googleDrive.data', 'w+') as data_file:
		for item in items:
			data_file.write('\t'.join([item['name'].encode('utf-8'), item['webViewLink'].encode('utf-8')]) + '\n')

def search_googleDriveData(term):
	results = []
	try:
		with open(program_path + 'googleDrive.data', 'r') as data_file:
			for line in data_file:
				if term.lower() in line.split('\t')[0].lower():
					results.append(line)
	except IOError:
		print 'Database not found, please use -u to create the database'
		exit(1)
	return results

if len(sys.argv) == 1:
	print "Parameter needed, program exit"
	exit(1)

if sys.argv[1] == '-u':
	update_googleDriveData()
	print 'Google drive data updated'
else:
	search_result = search_googleDriveData(sys.argv[1])
	if len(search_result) == 0:
		print "No match record found!"
	elif len(search_result) == 1:
		webbrowser.open_new(search_result[0].split('\t')[0])
	else:
		for i, item in enumerate(search_result):
			print ' '.join([str(i), item.split('\t')[0]])
		index = raw_input('index:> ')
		try:
			webbrowser.open_new(search_result[int(index)].split('\t')[1])
		except (IndexError, ValueError):
			print 'Invalid index'
