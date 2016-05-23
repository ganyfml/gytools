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
service = build('gmail', 'v1', http=credentials.authorize(Http()))

sent_or_not=sys.argv[2]
query=sys.argv[3]

exit_status=1

for email in sys.stdin:
	email = email.strip()
	res=service.users().messages().list(userId='me', q='to:%s from:me' % email).execute()
	if sent_or_not == 'no':
		if(res['resultSizeEstimate']==0):
			print email
			exit_status=0
	elif sent_or_not == 'yes':
		if(res['resultSizeEstimate']!=0):
			print email
			exit_status=0

sys.exit(exit_status)
