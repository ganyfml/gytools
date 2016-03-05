import smtplib
from selenium import webdriver
from email.mime.text import MIMEText
from pyvirtualdisplay import Display

def notice_thoughEmail():
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.ehlo()
    server.starttls()
    server.login( 'gany.fml@gmail.com', 'Gyge199049#' )
    msg = MIMEText("Check driver license")
    sender = 'gany@gmail.com'
    recipients = ['6122981354@tmomail.net', '4696003238@txt.att.net']
    msg['Subject'] = "Auto Generate"
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    server.sendmail(sender, recipients, msg.as_string())

#display = Display(visible=0, size=(800, 600))
#display.start()
browser = webdriver.Firefox()
browser.get('http://www.google.com/nexus/5x/')

button = browser.find_element_by_css_selector('.uppercase.button.inactive.gweb-smoothscroll-control')
button = button.text
print button_text
#display.stop()
