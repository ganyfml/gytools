#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from datetime import datetime
import requests
import time
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
	url = 'https://secure.thinkreservations.com/api/hotels/3300/daily_availabilities?start_date=2022-02-22&end_date=2022-02-23'
	res = requests.get(url)
	result = {}
	msg = 'No Room avaiable\n'
	for r in res.json():
		if not r['isAvailable']:
			continue
		if r['roomId'] in result:
			msg = 'Room avaiable\n'
			notice_thoughEmail(msg)
		else:
			result[r['roomId']] = True
	print_to_file(msg)

while True:
	now = datetime.now()
	print_to_file(now.strftime("%m/%d/%Y %H:%M:%S") + ':' + '\n')
	check_status()
	time.sleep(1800)
