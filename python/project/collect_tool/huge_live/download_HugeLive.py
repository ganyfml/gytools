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
from urllib.parse import urlsplit, urljoin
from utils.downloader import m3u8_downloader

#suppress youtube-dl print
class youtube_dl_quiet_logger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        pass

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
            else:
                pass
        d_info['ep'] = ep
        d_info['urls'] = ep2url[ep]
        download_infos.append(d_info)
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

def decode_duboku(url, src_name):
    def get_d_url_for_one_ep(ep_url, ep_txt, route_ep_d_info):
        res = requests.get(ep_url)
        d_url = re.search('"url":"(.*?m3u8)"', res.text).group(1).replace('\\', '')
        route_ep_d_info.append({ep_txt : d_url})

    url_data = requests.get(url)
    url_list = []
    soup = BeautifulSoup(url_data.text, 'html.parser')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        route_ep_d_info = []
        container = soup.find('ul', {'class' : 'myui-content__list'})
        processes = []
        for ep_li in container.find_all('li'):
            ep_info = ep_li.find('a')
            ep_url = urljoin(url,ep_info['href'])
            ep_txt = ep_info.text.strip()
            processes.append(pool.submit(get_d_url_for_one_ep, ep_url, ep_txt, route_ep_d_info))

    url_list.append(route_ep_d_info)

    video_title = soup.find('h1', {'class' : 'title'}).text.strip()
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
                ep_url = urljoin(url, ep_button['href'])
                ep_txt = ep_button.text.strip()
                pool.submit(get_d_url_for_one_ep, ep_url, ep_txt, route_ep_d_info)
        url_list.append(route_ep_d_info)

    video_title = soup.find('div', {'class' : 'video-title'}).text.strip()
    return video_title, url_list

def get_download_infos_from_URL(url, output_dir, src_name, file_prefix):
    xinghe_re = re.compile('hugelive|xinghe')
    duonao_re = re.compile('duonaolive')
    duboku_re = re.compile('gboku')
    if xinghe_re.search(url):
        video_title, url_list = decode_xinghe(url, src_name)
    elif duonao_re.search(url):
        video_title, url_list = decode_duonao(url, src_name)
    elif duboku_re.search(url):
        video_title, url_list = decode_duboku(url, src_name)
    else:
        print(f'URL not supported')
        return []

    download_infos = organize_download_urls(video_title, output_dir, url_list, file_prefix)
    print(f'{video_title} analysis complete')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return download_infos

def download_via_m3u8_downloader(d_output, d_file_prefix, d_ep, d_urls, verbose, pbar):
    d_file_name = f'{d_output}/{d_file_prefix}{d_ep:02d}.mp4'
    if os.path.isfile(d_file_name):
        return True

    download_success = False
    for u in d_urls:
        if verbose:
            pbar.write(f'Downloading: {u}')
        try:
            m3u8_downloader(u, d_file_name)
            download_success = True
        except:
            pass
    return download_success

def download_via_youtube_dl(d_output, d_file_prefix, d_ep, d_urls, verbose, pbar):
    ydl_opts = { 
        'nocheckcertificate': True, 
        'outtmpl': f'{d_output}/{d_file_prefix}{d_ep:02d}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'continue_dl': True,
        'logger': youtube_dl_quiet_logger()
    }

    youtube_dl.utils.std_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    download_success = False
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for u in d_urls:
            if verbose:
                pbar.write(f'Downloading: {u}')
            retry_count = 0
            while retry_count < 6:
                try:
                    ydl.download([u])
                    download_success = True
                    break
                except:
                    retry_count += 1
            if not download_success:
                pbar.write(f'Error downloading {d_title}: {d_ep} with {u}\nRetry: another url')
            else:
                pass
    return download_success

def download_task(v, verbose, pbar):
    d_title = v['title']
    d_urls = v['urls']
    d_ep = v['ep']
    d_file_prefix = v['file_prefix']
    d_output = v['output']
    pbar.write(f'Start Downloading {d_title} {d_ep:02d}')

    #download_success = download_via_youtube_dl(d_output, d_file_prefix, d_ep, d_urls, verbose, pbar)
    download_success = download_via_m3u8_downloader(d_output, d_file_prefix, d_ep, d_urls, verbose, pbar)
    if download_success:
        pbar.write(f'{d_title} {d_ep} Finish')
    else:
        pbar.write(f'{d_title} {d_ep} download Failed')
    pbar.update(1)
    return d_title, d_ep, download_success

def download_multiple(url_list, verbose):
    pbar = tqdm(total=len(url_list), desc='Downloading:')
    error_list = []
    processes = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
        for url in url_list:
            processes.append(e.submit(download_task, url, verbose, pbar))
        for _ in concurrent.futures.as_completed(processes):
            titile, ep, success = _.result()
            if not success:
                error_list.append(f'{titile}: {ep}')
        print(f'{len(error_list)} task failed:')
        print('\n'.join(error_list))

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

    download_infos = []
    if args.read:
        with open(args.read, 'r') as f:
            download_links = yaml.load(f, Loader=yaml.FullLoader)
        for l in download_links:
            download_infos.extend(get_download_infos_from_URL(l['url'], l['path'], args.src, l['prefix'] if 'prefix' in l else ''))
    else:
        download_infos = get_download_infos_from_URL(args.input, args.output, args.src, args.prefix if 'prefix' in args else '')

    print(f'{len(download_infos)} video found, start downloading')

    duboku_re = re.compile('gboku')
    d_func = None
    download_multiple(download_infos, args.verbose)
