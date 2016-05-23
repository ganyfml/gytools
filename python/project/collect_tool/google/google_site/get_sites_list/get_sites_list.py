import os
import gdata.sites.client
import gdata.gauth

domain = sys.argv[1]
tokencache = sys.argv[2]

if domain == '':
  client = gdata.sites.client.SitesClient()
else:
  client = gdata.sites.client.SitesClient(domain=domain)

with open(tokencache, 'r') as f:
  saved_blob_string = f.read().strip()
  token = gdata.gauth.token_from_blob(saved_blob_string)
  token.authorize(client)
  feed = client.GetSiteFeed()
  for entry in feed.entry:
    print "%s" % (entry.GetAlternateLink().href)
