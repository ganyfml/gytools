#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

def save_file_fromURL(url, path):
	try:
		r = requests.get(url, stream=True)
		if r.status_code == 200:
			with open(path, 'wb') as f:
				for chunk in r:
					f.write(chunk)
	except:
		print "Error Detected, one image ignored"
