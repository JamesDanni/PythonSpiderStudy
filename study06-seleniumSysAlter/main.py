#coding=utf-8

from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
from datetime import datetime

#签到xpath
sign_in = '//*[@id="form1"]/div[3]/table[1]/tbody/tr[2]/td[1]/img'
#签退xpath
sign_out = '//*[@id="form1"]/div[3]/table[1]/tbody/tr[2]/td[3]/img'

def calc_data():
    pass

def calc_time():
    pass

def open_chorm():
    dv = webdriver.Chrome()
    dv.maximize_window()
    wait = ui.WebDriverWait(dv, 10)
    dv.get("http://oa.founder.com/group/Comperhensive/Default.aspx")
    time.sleep(5)
    tc = dv.switch_to.alert()
    tc.accept()
    time.sleep(120)  # 公司连北京服务器，会比较慢，这里直接等2min

def main():
    open_chorm()

main()

today = datetime.now().weekday() + 1

