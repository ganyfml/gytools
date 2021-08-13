#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from datetime import datetime
import requests
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

recipients = ['gany.fml@gmail.com']
def notice_thoughEmail(message):
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.ehlo()
  server.starttls()
  server.login('email', 'password')
  msg = MIMEText(message)
  sender = 'gany@gmail.com'
  msg['Subject'] = message
  msg['From'] = sender
  msg['To'] = ", ".join(recipients)
  server.sendmail(sender, recipients, msg.as_string())

def print_to_file(msg):
	with open('out.txt', 'a') as f:
		f.write(msg)

def check_status():
	url = 'https://poconoonline.adventureres.com/responsive/index.php?locationId=3&resDate=8/28/2021&serviceGroupId=9'

	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	ele = soup.find_all('div', {'class' : 'service-choice-time'})
	if len(ele) == 0:
		print_to_file('no available spot\n')
		return

	options = ele[0].find_all('option')
	for t in options:
		if not t.has_attr('data-availability'):
			continue
		num_spot = int(t['data-availability'])
		spot_time = t['data-datetimestr']
		msg = spot_time + ':    ' + str(num_spot) + '\n'
		print_to_file(msg)
		if num_spot >= 6:
			notice_thoughEmail(msg)

while True:
	now = datetime.now()
	print_to_file(now.strftime("%m/%d/%Y %H:%M:%S") + ':' + '\n')
	check_status()
	time.sleep(60)
