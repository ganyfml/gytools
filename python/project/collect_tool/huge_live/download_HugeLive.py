#!/usr/bin/python
import os
import threading
import requests, re
import sys
import js2py
import json
import youtube_dl
import concurrent.futures
import argparse

download_url = sys.argv[1]
download_path = sys.argv[2]

def get_download_link_from_URL(url)
	##Download the encrypted_data
	url_data = requests.get(url)
	encrypted_data = re.search(r'{"dataEnc":"(.*?)"', url_data.text).group(1)

	##Decode the data
	with open('decode.js','r') as f:
		js_decode_func = js2py.eval_js(f.read())
		decode_data = js_decode_func(encrypted_data)
		src_pangzi = json.loads(decode_data['pangzi_info'])
		url_list = json.loads(src_pangzi[0]['srcs'])
	return url_list

def download_task(v, output_dir):
	v_index = list(v.keys())[0]
	ydl_opts = { 
		'nocheckcertificate': True, 
		'outtmpl': f'{output_dir}/{v_index}.%(ext)s',
		'quiet': True,
		'no_warnings': True,
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print(v[v_index])
		ydl.download([v[v_index]])

def download_multiple(url_list, path):
	with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
		for url in url_list:
			e.submit(download_task, url, path)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Download videos from hugelive.com')

	parser.add_argument('-r', '--read', help='Download multiple tv/movie series using yaml file', required=False)

	parser.add_argument('-i', '--input', help='tv/movie url to download from', required=False)
	parser.add_argument('-o', '--output', help='path to store the downloaded file', required=False)
	args = parser.parse_args()


	if args.read and (args.input or args.out):
		print("Download either using -i and -o or using config file")
		sys.exit(2)

	else if not args.read and (not args.input or not args.out):
		print("Download single file must provide both -i and -o")
		sys.exit(2)

	if args.read:
		sys.exit(2)
	else:
		print('extracting video urls')
		url_list = get_download_link_from_URL(args.input)
		print(f'{len(url_list)} video urls found')
		download_multiple(url_list, args.output)
