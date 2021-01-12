#!/usr/bin/python

import requests, re, time, datetime
from win10toast import ToastNotifier
import winsound

sound_frequency = 2500
sound_duration = 1000
toaster = ToastNotifier()

url = 'https://www.shopskibluemt.com/intouchPrices/list'
data = {'productForm' : 'product_attribute_3603=&product_attribute_3602=&product_attribute_3628-startdate=&product_attribute_3628-price=0&product_attribute_3628=&addtocart_579.EnteredQuantity=1', 'start': '2021-01-12', 'end': '2021-02-07'}

def check_res(res):
    ret = []
    for p in res:
        o_display = p['optionDisplay']
        if o_display.find('1/16/2021') != -1 and int(re.search('(\d+) Remaining', o_display).groups()[0]) >= 2:
            ret = [p['optionDisplay']]
            break
    return ret

count = 0
while True:
    four_hour = dict(data)
    four_hour['productId'] = 579

    eight_hour = dict(data)
    eight_hour['productId'] = 582

    four_hour_res = requests.post(url, four_hour)
    eight_hour_res = requests.post(url, eight_hour)

    find_res = []
    find_res = find_res + check_res(four_hour_res.json())
    find_res = find_res + check_res(eight_hour_res.json())

    with open('ski.log', 'a') as the_file:
        now = datetime.datetime.now()
        the_file.write('last_check: ' + now.strftime("%d/%m/%Y %H:%M:%S") + '\n')

        if(len(find_res) != 0):
            winsound.Beep(sound_frequency, sound_duration)
            toaster.show_toast("Res found",'\n'.join(find_res))
            the_file.write("res_found：" + ' '.join(find_res) + '\n')

        the_file.write('count: ' + str(count) + '\n')

    count += 1
    time.sleep(20)