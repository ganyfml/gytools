# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import m3u8
import requests
from urllib.parse import urlsplit, urljoin
import tempfile
from shutil import rmtree
import cfscrape
import subprocess
import os
import concurrent.futures
import time

global GLOBAL_STOP
GLOBAL_STOP = False

requests.packages.urllib3.disable_warnings() 

class DownloadFailException(Exception):
    def __init__(self, status_code, message='Download failed'):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}, Error code: {self.status_code}'

def d_ts_segment(url, ts_file, segment):
    global GLOBAL_STOP
    if GLOBAL_STOP:
        return

    retry_c = 0
    response = None
    while retry_c < 5:
        response = requests.get(url, verify=False)
        if not response.ok and response.text.find('Cloudflare') != -1:
            scraper = cfscrape.create_scraper()
            response = scraper.get(url)

        if response.ok:
            break
        else:
            retry_c += 1
            time.sleep(5)

    if not response or not response.ok:
        GLOBAL_STOP = True
        raise DownloadFailException(response.status_code)
    
    with open(ts_file, 'wb') as f:
        f.write(response.content)
    segment.uri = ts_file

def m3u8_downloader(m3u8_url, saved_name):
    m3u8_info = m3u8.load(m3u8_url, verify_ssl=False)
    if len(m3u8_info.playlists) != 0:
        p_list_m3u8_url = urljoin(m3u8_url, m3u8_info.playlists[0].uri)
        m3u8_info = m3u8.load(p_list_m3u8_url, verify_ssl=False)
    
    tmp_d = tempfile.mkdtemp()
    if len(m3u8_info.keys) != 0 and m3u8_info.keys[0]:
        key_url = urljoin(m3u8_url, m3u8_info.keys[0].uri)
        key = requests.get(key_url, verify=False).content
        key_file = os.path.join(tmp_d, 'key.key')
        with open(key_file, 'wb') as f:
            f.write(key)
        m3u8_info.keys[0].uri = key_file

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
        processes = []
        for s in m3u8_info.segments:
            s_url = urljoin(m3u8_url, s.uri)
            ts_file_name = os.path.basename(s_url)
            ts_file = os.path.join(tmp_d, ts_file_name)
            processes.append(e.submit(d_ts_segment, s_url, ts_file, s))
    
    ffmpeg_error_code = 0
    if not GLOBAL_STOP:
        m3u8_file_name = os.path.join(tmp_d, 'index.m3u8')
        m3u8_info.dump(m3u8_file_name)
        cmd = ['ffmpeg', '-allowed_extensions', 'ALL', '-i', m3u8_file_name, '-c', 'copy', saved_name]
        handle = subprocess.Popen(
                cmd, stderr=subprocess.PIPE,
                stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_data, stderr_data = handle.communicate()
        ffmpeg_error_code = handle.returncode

    rmtree(tmp_d, ignore_errors=True)
    if GLOBAL_STOP or ffmpeg_error_code != 0:
        raise Exception('Download failed')
