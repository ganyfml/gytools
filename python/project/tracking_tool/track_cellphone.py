import smtplib
from selenium import webdriver
from email.mime.text import MIMEText

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

browser = webdriver.Firefox()
browser.get('https://store.google.com/product/nexus_6')
browser.find_element_by_xpath("//button[@class='button primary transaction']").click()
browser.find_element_by_xpath("//button[@class='non-selectable color-option-radio']").click()
browser.find_element_by_xpath("//button[@class='non-selectable spacer']").click()
browser.find_element_by_xpath("//button[@class='large transaction summary-button button id-add-to-cart-button']").click()
browser.find_element_by_xpath("//button[@class='transaction large id-checkout-button checkout-button']").click()
file = open('source.html', 'w')
file.write(browser.page_source.encode('ascii', 'ignore'))
