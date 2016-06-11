#!/usr/bin/env python
# vim: set noexpandtab tabstop=2:

import oauth2client.file
import oauth2client.client
import oauth2client.tools

import sys

import argparse
flags = argparse.Namespace()
flags.logging_level='ERROR'
flags.noauth_local_webserver=True

clientsecrets_path=sys.argv[1]
credential_path=sys.argv[2]

flow = oauth2client.client.flow_from_clientsecrets(filename=clientsecrets_path, scope='https://www.googleapis.com/auth/drive.metadata.readonly')
storage = oauth2client.file.Storage(filename=credential_path)

oauth2client.tools.run_flow(flow=flow, storage=storage, flags=flags)
