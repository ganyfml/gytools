#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import smtplib
from email.mime.text import MIMEText
import requests
import re
import datetime

recipients = ['gany.fml@gmail.com']
def notice_thoughEmail(message):
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.ehlo()
	server.starttls()
	server.login( 'email', 'password' )
	msg = MIMEText(message)
	sender = 'gany@gmail.com'
	msg['Subject'] = message
	msg['From'] = sender
	msg['To'] = ", ".join(recipients)
	server.sendmail(sender, recipients, msg.as_string())

base_url = 'https://booknow.securedata-trans.com/1qed83ds/'
payload_template = {
		'customer_location_id' : 553
		, 'headquarters_id' : 2
		, 'id' : 553
		, 'location_id' : 553
		, 'date_ymd' : 20160932
		, 'service_id' : 2
		}
def get_earliest_day_in_month(year, month):
	payload = payload_template
	payload['date_ymd'] = '%d%02d32' % (year, month)
	r = requests.get('https://booknow.securedata-trans.com/1qed83ds/', payload_template)
	try:
		return int(re.finditer('<a id="cv-leftnav-item-calendar-available-id".*>(\d*)<\/a>', r.text).next().group(1))
	except StopIteration:
		return None

now = datetime.datetime.now()
def get_earliest_date():
	year = now.year
	month = now.month
	for i in range(10):
		new_month = month % 12 + 1
		year += new_month < month
		month = new_month
		day = get_earliest_day_in_month(year, month)
		return datetime.datetime(year, month, day)

prev_date = get_earliest_date()
#notice_thoughEmail('old time expried, new time: ' + time.strptime(new_date, '%d/%m/%Y')
print 'Init the program, start date: ' + '%d/%d/%d' % (prev_date.month, prev_date.day, prev_date.year)
while True:
	new_date = get_earliest_date()
	if new_date > prev_date:
		#notice_thoughEmail('old time expried, new time: ' + time.strptime(new_date, '%d/%m/%Y')
		print 'old time expried, new time: ' + '%d/%d/%d' % (new_date.month, new_date.day, new_date.year)
	elif new_date < prev_date:
		#notice_thoughEmail('!!!! New time avaiable on ' + time.strptime(new_date, '%d/%m/%Y')
		print '!!!! New time avaiable on ' + '%d/%d/%d' % (new_date.month, new_date.day, new_date.year)
	new_date = prev_date
	print new_date
