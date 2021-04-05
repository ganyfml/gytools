# vim: set noexpandtab tabstop=4 shiftwidth=4 softtabstop=-1 fileencoding=utf-8:

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


class DownloadFailException(Exception):
	def __init__(self, status_code, message='Download failed'):
		self.status_code = status_code
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		return f'{self.message}, Error code: {self.status_code}'

class m3u8Downloader():
	def __init__(self, config = None):
		if config:
			self.config = config
		else:
			self.config = {
				'max_workers': 4
			}

		self.global_stop = False
		self.scraper = cfscrape.create_scraper()
		requests.packages.urllib3.disable_warnings() 

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		pass

	def __d_ts_segment(self, url, ts_file, segment):
		if self.global_stop:
			return
	
		retry_c = 0
		response = None
		while retry_c < 5:
			response = self.scraper.get(url)
	
			if response.ok:
				break
			else:
				retry_c += 1
				time.sleep(5)
	
		if not response or not response.ok:
			raise DownloadFailException(response.status_code)
		
		with open(ts_file, 'wb') as f:
			f.write(response.content)
		segment.uri = ts_file
	
	def __download_helper(self, m3u8_url, saved_name, tmp_d):
		if os.path.isfile(saved_name):
			return 1, 'file exist'
	
		m3u8_info = m3u8.load(m3u8_url, verify_ssl=False)
		if len(m3u8_info.playlists) != 0:
			p_list_m3u8_url = urljoin(m3u8_url, m3u8_info.playlists[0].uri)
			m3u8_info = m3u8.load(p_list_m3u8_url, verify_ssl=False)
		
		if len(m3u8_info.keys) != 0 and m3u8_info.keys[0]:
			key_url = urljoin(m3u8_url, m3u8_info.keys[0].uri)
			key = requests.get(key_url, verify=False).content
			key_file = os.path.join(tmp_d, 'key.key')
			with open(key_file, 'wb') as f:
				f.write(key)
			m3u8_info.keys[0].uri = key_file
	
		future_list = []
		with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['max_workers']) as e:
			for s in m3u8_info.segments:
				s_url = urljoin(m3u8_url, s.uri)
				ts_file_name = os.path.basename(s_url)
				ts_file = os.path.join(tmp_d, ts_file_name)
				future_list.append(e.submit(self.__d_ts_segment, s_url, ts_file, s))
		
		#If any segment failed, throw exception
		for future in concurrent.futures.as_completed(future_list):
			try:
				future.result()
			except Exception:
				self.global_stop = True
				raise
		
		if not self.global_stop:
			m3u8_file_name = os.path.join(tmp_d, 'index.m3u8')
			m3u8_info.dump(m3u8_file_name)
			cmd = ['ffmpeg', '-allowed_extensions', 'ALL', '-i', m3u8_file_name, '-c', 'copy', saved_name]
			handle = subprocess.Popen(
					cmd, stderr=subprocess.PIPE,
					stdout=subprocess.PIPE, stdin=subprocess.PIPE)
			stdout_data, stderr_data = handle.communicate()
			ffmpeg_error_code = handle.returncode
		
			if ffmpeg_error_code != 0:
				return -1, 'ffmpeg download failed'
	
		return 0, 'success'
	
	def download(self, m3u8_url, saved_name):
		tmp_d = tempfile.mkdtemp()
		try:
			return self.__download_helper(m3u8_url, saved_name, tmp_d)
		except DownloadFailException as e:
			return -1, str(e)
		finally:
			rmtree(tmp_d, ignore_errors=True)
