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
from tqdm import tqdm
from bs4 import BeautifulSoup

def organize_download_urls(video_title, output_dir, url_list, file_prefix):
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
                num_extract = re.findall(r'\d+', m_key)
                if len(num_extract) == 1:
                    m_key = int(num_extract[0])
                else:
                    pass
            
            if m_key in ep2url:
                ep2url[m_key].append(m_value)
            else:
                ep2url[m_key] = [m_value]

    for u in url_list[0]:
        d_info = {
             'title': video_title,
             'ep': list(u.keys())[0],
             'output': output_dir,
             'file_prefix': file_prefix
             }
        raw_ep = list(u.keys())[0]
        ep = raw_ep
        try:
            ep = int(raw_ep)
        except:
            num_extract = re.findall(r'\d+', raw_ep)
            if len(num_extract) == 1:
                ep = int(num_extract[0])
                d_info['urls'] = ep2url[ep]
                download_infos.append(d_info)
            else:
                pass
    return download_infos

def decode_xinghe(url, src_name):
    #l5_info temp down due to duboku cannot download
    src_orders = ['l4_info', 'l8_info', 'l1_info']
    
    ##Download the encrypted_data
    url_data = requests.get(url)
    encrypted_data = re.search(r'{"data":"(.*?)"', url_data.text).group(1)

    ##Decode the data
    with open('decode.js','r') as f:
        js_decode_func = js2py.eval_js(f.read())
        decode_data = js_decode_func(encrypted_data)['results']
        url_list = []

        src2process = [src_name] if src_name else src_orders
        for src in src2process:
            if src not in decode_data:
                print(f'{src} not avaiable')
                continue
            src_info = json.loads(decode_data[src])
            if len(src_info) != 0:
                url_list.append(json.loads(src_info[0]['srcs']))

        if len(url_list) == 0:
            print('No avaiable srcs found, abort')
            return []

        video_title = json.loads(decode_data['infos'])[0]["title"]
    return video_title, url_list

def decode_duonao(url, src_name):
    def get_d_url_for_one_ep(ep_url, ep_txt, route_ep_d_info):
        res = requests.get(ep_url)
        d_url = re.search(r"video_url: \'(.*)\'", res.text).group(1)
        route_ep_d_info.append({ep_txt : d_url})

    url_data = requests.get(url)
    routes = [m.group(1) for m in re.finditer('href="#route(\d)"', url_data.text)]
    print(f'{len(routes)} route(s) found, analysing')
    url_list = []
    soup = BeautifulSoup(url_data.text, 'html.parser')
    for r in routes:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            route_ep_d_info = []
            container = soup.find('div', {'id' : f'route{r}'})
            for ep_button in container.find_all('a'):
                ep_url = ep_button['href'].replace('../', 'https://duonaolive.com/')
                ep_txt = ep_button.text.strip()
                pool.submit(get_d_url_for_one_ep, ep_url, ep_txt, route_ep_d_info)
        url_list.append(route_ep_d_info)

    video_title = soup.find('div', {'class' : 'video-title'}).text.strip()
    return video_title, url_list

def get_download_infos_from_URL(url, output_dir, src_name, file_prefix):
    xinghe_re = re.compile('hugelive|xinghe')
    duonao_re = re.compile('duonaolive')
    if xinghe_re.search(url):
        video_title, url_list = decode_xinghe(url, src_name)
    elif: duonao_re.search(url):
        video_title, url_list = decode_duonao(url, src_name)
    else:
        print(f'URL not supported')
        return []

    download_infos = organize_download_urls(video_title, output_dir, url_list, file_prefix)
    print(f'{video_title} analysis complete')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return download_infos

def download_task(v, verbose, pbar):
    d_title = v['title']
    d_urls = v['urls']
    d_ep = v['ep']
    d_file_prefix = v['file_prefix']
    d_output = v['output']
    pbar.write(f'Start Downloading {d_title} {d_ep}')
    ydl_opts = { 
        'nocheckcertificate': True, 
        'outtmpl': f'{d_output}/{d_file_prefix}{d_ep}.%(ext)s',
        'quiet': True,
        'no_warnings': True
    }
    download_success = False
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for u in d_urls:
            try:
                if verbose:
                    pbar.write(f'Downloading: {u}')
                ydl.download([u])
                download_success = True
                break
            except:
                pbar.write(f'Error downloading {v['title']} with {v['urls']}\nRetry: {v['title']} with another url')
                pass
    if download_success:
        pbar.write(f'{d_title} {d_ep} Finish')
    else:
        pbar.write(f'{d_title} {d_ep} download Failed')
    pbar.update(1)

def download_multiple(url_list, verbose):
    pbar = tqdm(total=len(url_list), desc='Downloading:')
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
        for url in url_list:
            e.submit(download_task, url, verbose, pbar)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download videos from hugelive.com')

    parser.add_argument('-r', '--read', help='Download multiple tv/movie series using yaml file', required=False)

    parser.add_argument('-s', '--src', help='Sepcific source to download', required=False)

    parser.add_argument('-i', '--input', help='tv/movie url to download from', required=False)
    parser.add_argument('-o', '--output', help='path to store the downloaded file', required=False)
    parser.add_argument('-p', '--prefix', help='downloaded file prefix', required=False)

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
            download_infos.extend(get_download_infos_from_URL(l['url'], l['path'], args.src, l['prefix'] if 'prefix' in l else ''))
    else:
        download_infos = get_download_infos_from_URL(args.input, args.output, args.src, args.prefix if 'prefix' in args else '')

    print(f'{len(download_infos)} video found, start downloading')
    download_multiple(download_infos, args.verbose)
