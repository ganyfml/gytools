#!/usr/bin/python
import os
import threading
import requests, re
import sys
import js2py
import json
import youtube_dl
import concurrent.futures

download_url = sys.argv[1]
download_path = sys.argv[2]

##Download the encrypted_data
url_data = requests.get(download_url)
encrypted_data = re.search(r'{"dataEnc":"(.*?)"', url_data.text).group(1)

##Decode the data
with open('decode.js','r') as f:
	js_decode_func = js2py.eval_js(f.read())
	decode_data = js_decode_func(encrypted_data)
	src_pangzi = json.loads(decode_data['pangzi_info'])
	url_list = json.loads(src_pangzi[0]['srcs'])

def download_task(v, output_dir):
	v_index = list(v.keys())[0]
	ydl_opts = { 
		'nocheckcertificate': True, 
		'outtmpl': f'{output_dir}/{v_index}.%(ext)s'
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print(v[v_index])
		ydl.download([v[v_index]])


if __name__ == "__main__":
	output_dir = "C:/Users/ganyf/Desktop/test"

	with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
		for url in url_list:
			e.submit(download_task, url, output_dir)