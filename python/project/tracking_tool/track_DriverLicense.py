from pyvirtualdisplay import Display
import smtplib
from selenium import webdriver
from email.mime.text import MIMEText
import time

MONTH = {'February': '2', 'March': '3', 'April': '4', 'May': '5'}

def notice_thoughEmail(message):
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.ehlo()
    server.starttls()
    server.login( 'email', 'password' )
    msg = MIMEText(message)
    sender = 'gany@gmail.com'
    recipients = ['6122981354@tmomail.net']
    msg['Subject'] = message
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    server.sendmail(sender, recipients, msg.as_string())

send_message = False
first_time = True
browser = webdriver.Firefox()
day = 999
month = 999
while not send_message:
    browser.get('https://booknow.securedata-trans.com/1qed83ds/')
    browser.find_element_by_xpath("//select/option[contains(.,'Regular')]").click()
    source = browser.page_source
    source_content = str(source.encode('ascii','ignore'))
    while "calendar-available" not in source_content:
        browser.find_element_by_xpath("//*[@id='calendar']/tbody/tr[1]/th[3]/a").click()
        source = browser.page_source
        source_content = str(source.encode('ascii','ignore'))

    new_day = int(browser.find_element_by_id('cv-leftnav-item-calendar-available-id').text.encode('ascii','ignore'))
    new_month = int(MONTH[str(browser.find_element_by_xpath('//*[@id="calendar"]/tbody/tr[1]/th[2]/span').text.encode('ascii','ignore')).split(' ', 1)[0]])

    if(first_time):
        day = new_day
        month = new_month
        first_time = False
        print "First time complete"
        old_date = "Old Date record: " + str(month) + '/' + str(day)
        print old_date
    else:
        if new_month < month:
            send_message = True
        elif new_month == month and new_day < day:
            send_message = True
        if send_message:
            message = "New Date avaiable: " + str(new_month) + '/' + str(new_day)
            print message
            notice_thoughEmail(message)
        else:
            print "No new data avaiable"
