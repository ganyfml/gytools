# vim: set noexpandtab tabstop=4 shiftwidth=4 softtabstop=-1 fileencoding=utf-8:

import requests, yaml

def send_by_spontit(title, content):
	config = None
	with open('/home/gany/.bin/config.yml') as f:
		config = yaml.safe_load(f)

	headers = {
		'Content-Type': 'application/json',
		'X-Authorization': config['api_key'],
		'X-UserId': config['user_name']
	}

	payload = {
		'pushTitle': title,
		'content': content
	}

	p = requests.post('https://api.spontit.com/v3/push', data = payload, headers = headers)
