import os
import gdata.sites.client
import gdata.sites.data
import gdata.gauth

#Place to store the cached token
token_cache_path = os.environ['HOME'] + '/.gdata-storage'
print "Token Cache: %s" % token_cache_path

try:
    #Try to read token locally
    with open(token_cache_path, 'r') as f:
        saved_blob_string = f.read()
       if saved_blob_string is not None:
           token = gdata.gauth.token_from_blob(saved_blob_string)
       else:
           token = None
except IOError:
    token = None

if token == None :
    #No avaiable token has been readed
   print "Getting a new token."
   token = gdata.gauth.OAuth2Token( client_id=client_id,
           client_secret=client_secret,
           scope='https://sites.google.com/feeds/',
           user_agent='acaird-acexample-v1')
   url = token.generate_authorize_url(redirect_uri='urn:ietf:wg:oauth:2.0:oob')
   print 'Please go to the URL below and authorize this '
   print 'application, then enter the code it gives you.'
   print '   %s' % url
   code = raw_input("Code: ")
   token.get_access_token(code)
   client = gdata.sites.client.SitesClient(source='acaird-acexample-v1', site='acaird')
   token.authorize(client)
   saved_blob_string = gdata.gauth.token_to_blob(token)
   f=open (token_cache_path, 'w')
   f.write(saved_blob_string)
else:
    print "Using a cached token from %s" % token_cache_path
   client = gdata.sites.client.SitesClient(source='acaird-acexample-v1', site='acaird')
   token.authorize(client)

f.close()
