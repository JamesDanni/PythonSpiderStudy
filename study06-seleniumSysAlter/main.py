#coding=utf-8

from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
from datetime import datetime

#签到xpath
sign_in = '//*[@id="form1"]/div[3]/table[1]/tbody/tr[2]/td[1]/img'
#签退xpath
sign_out = '//*[@id="form1"]/div[3]/table[1]/tbody/tr[2]/td[3]/img'

def calc_time():
    time_now = time.strftime("%H:%M:%S", time.localtime())
    if time_now > "17:45:00":  #TODO 签到的时间区域
        return sign_in
    if time_now < "17:49:50":  #TODO 签退的时间区域
        return sign_out
    return ""

def open_chorm(want_xpath):
    dv = webdriver.Chrome()
    dv.maximize_window()
    wait = ui.WebDriverWait(dv, 10)
    dv.get("http://oa.founder.com/group/Comperhensive/Default.aspx")
    time.sleep(5)
    tc = dv.switch_to.alert()
    tc.accept()
    time.sleep(120)  # 公司连北京服务器，会比较慢，这里直接等2min
    try:
        dv.find_element_by_xpath(want_xpath).click()
    except:
        dv.close()
        return False
    dv.close()
    return True

def main():
    # open_chorm()
    want_xpaht = calc_time()
    if want_xpaht == "":
        time.sleep(500)
        return
    else:
        should_again = True
        while should_again:
            should_again = open_chorm(want_xpaht)

while 1:
    main()

today = datetime.now().weekday() + 1

