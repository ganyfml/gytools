from pyvirtualdisplay import Display
import smtplib
from selenium import webdriver
from email.mime.text import MIMEText

def notice_thoughEmail():
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.ehlo()
    server.starttls()
    server.login( 'email', 'password' )
    msg = MIMEText("Check driver license")
    sender = 'gany@gmail.com'
    recipients = ['6122981354@tmomail.net', '4696003238@txt.att.net']
    msg['Subject'] = "Auto Generate"
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    server.sendmail(sender, recipients, msg.as_string())

display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Firefox()
browser.get('https://booknow.securedata-trans.com/1qed83ds/')
browser.find_element_by_xpath("//select/option[contains(.,'Regular')]").click()
source = browser.page_source
source_content = str(source.encode('ascii','ignore'))
if "calendar-available" in source_content:
    notice_thoughEmail()
browser.quit()
display.stop()
