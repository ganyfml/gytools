#!/usr/bin/python3

import os
import threading
import requests, re
import sys
import js2py
import json
import youtube_dl
import concurrent.futures
import argparse
import yaml

def get_download_infos_from_URL(url, output_dir):
    src_orders = ['pangzi_info', 'pangzi_info_backup', 'cjg_info', 'zuikuai_info', 'mahua_info']
    
    ##Download the encrypted_data
    url_data = requests.get(url)
    encrypted_data = re.search(r'{"dataEnc":"(.*?)"', url_data.text).group(1)

    ##Decode the data
    with open('decode.js','r') as f:
        js_decode_func = js2py.eval_js(f.read())
        decode_data = js_decode_func(encrypted_data)
        url_list = []
        for src in src_orders:
            src_info = json.loads(decode_data[src])
            if len(src_info) != 0:
                url_list = json.loads(src_info[0]['srcs'])
                break;
        if len(url_list) == 0:
            print('No srcs found, abort')
            return []

        download_infos = []
        video_info = json.loads(decode_data['infos'])[0]
        for u in url_list:
            download_infos.append({
                'title': video_info['title'],
                'ep': list(u.keys())[0],
                'url': list(u.values())[0],
                'output': output_dir
                })
        print(f'{video_info["title"]} analysis complete')

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    return download_infos

def download_task(v, verbose):
    d_title = v['title']
    d_url = v['url']
    d_ep = v['ep']
    d_output = v['output']
    print(f'Start Downloading {d_title} {d_ep}')
    ydl_opts = { 
        'nocheckcertificate': True, 
        'outtmpl': f'{d_output}/{d_ep}.%(ext)s',
        'quiet': True
        # 'no_warnings': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        if verbose:
            print(f'Downloading: {d_url}')
        ydl.download([d_url])
    print(f'{d_title} {d_ep} Finish')

def download_multiple(url_list, verbose):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
        for url in url_list:
            e.submit(download_task, url, verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download videos from hugelive.com')

    parser.add_argument('-r', '--read', help='Download multiple tv/movie series using yaml file', required=False)

    parser.add_argument('-i', '--input', help='tv/movie url to download from', required=False)
    parser.add_argument('-o', '--output', help='path to store the downloaded file', required=False)

    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode', required=False)

    parser.add_argument('-a', '--analysis', action='store_true', help='analysis mode', required=False)
    args = parser.parse_args()

    if args.read and (args.input or args.output):
        print("Download either using -i and -o or using config file")
        sys.exit(2)

    elif not args.read and (not args.input or not args.output):
        print("Download single file must provide both -i and -o")
        sys.exit(2)

    if args.read:
        with open(args.read, 'r') as f:
            download_links = yaml.load(f, Loader=yaml.FullLoader)
        download_infos = []
        for l in download_links:
            download_infos.extend(get_download_infos_from_URL(l['url'], l['path']))
    else:
        download_infos = get_download_infos_from_URL(args.input, args.output)

    print(f'{len(download_infos)} video found, start downloading')
    download_multiple(download_infos, args.verbose)
