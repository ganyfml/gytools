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

def organize_download_urls(video_info, output_dir, url_list):
    download_infos = []
    ep2url = {}
    for u in url_list:
        for m in u:
            m_raw_key = list(m.keys())[0]
            m_value = m[m_raw_key]
            m_key = m_raw_key
            try:
                m_key = int(m_key)
            except ValueError:
                pass
            
            if m_key in ep2url:
                ep2url[m_key].append(m_value)
            else:
                ep2url[m_key] = [m_value]
    
    for u in url_list[0]:
        d_info = {
             'title': video_info['title'],
             'ep': list(u.keys())[0],
             'output': output_dir,
             }
        raw_ep = list(u.keys())[0]
        ep = raw_ep
        try:
            ep = int(raw_ep)
        except:
            pass
        d_info['urls'] = ep2url[ep]
        download_infos.append(d_info)
    print(download_infos)
    return download_infos

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
                url_list.append(json.loads(src_info[0]['srcs']))
        if len(url_list) == 0:
            print('No srcs found, abort')
            return []

        video_info = json.loads(decode_data['infos'])[0]
        download_infos = organize_download_urls(video_info, output_dir ,url_list)
        print(download_infos)
        print(f'{video_info["title"]} analysis complete')

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    return download_infos

def download_task(v, verbose):
    d_title = v['title']
    d_urls = v['urls']
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
        for u in d_urls:
            try:
                if verbose:
                    print(f'Downloading: {u}')
                ydl.download([u])
                break
            except:
                print('retry: ')
                pass
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
