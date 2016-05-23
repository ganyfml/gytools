#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import gdata.gauth
import json
import sys

credential = sys.argv[1]
with open(credential) as data_file:
  data = json.load(data_file)
  client_id = data["installed"]["client_id"]
  client_secret = data["installed"]["client_secret"]

token = gdata.gauth.OAuth2Token(
    client_id=client_id
    , client_secret=client_secret
    , scope='https://sites.google.com/feeds'
    , user_agent='a'
    )
url = token.generate_authorize_url(
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    ,access_type='offline'
    ,approval_prompt='force')

print >> sys.stderr, """
Please go to the URL below and authorize this application, then enter the code it gives you.

   %s

""" % url

sys.stderr.write('Code: ')
code = raw_input()
token.get_access_token(code)
saved_blob_string = gdata.gauth.token_to_blob(token)
print "token: " + saved_blob_string
