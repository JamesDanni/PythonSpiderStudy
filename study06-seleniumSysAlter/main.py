#coding=utf-8

from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
from datetime import datetime
import logging
import random

logging.basicConfig(level = "ERROR",
                    datefmt = "%Y-%m-%d %H:%M:%S",
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    filename = "/log.txt",
                    filemode = 'w'
                    )

#签到xpath
sign_in = '//*[@id="form1"]/div[3]/table[1]/tbody/tr[2]/td[1]/img'
#签退xpath
sign_out = '//*[@id="form1"]/div[3]/table[1]/tbody/tr[2]/td[3]/img'

def calc_time():
    time_now = time.strftime("%H:%M:%S", time.localtime())
    if time_now > "08:15:00" and time_now < "08:30:00":
        time.sleep(random.randint(60,480))
        return sign_in
    if time_now > "17:30:00" and time_now < "18:00:00":
        time.sleep(random.randint(60,480))
        return sign_out
    return ""

def open_chorm(want_xpath):
    dv = webdriver.Chrome()
    dv.maximize_window()
    wait = ui.WebDriverWait(dv, 10)
    dv.get("http://oa.founder.com/group/Comperhensive/Default.aspx")
    logging.error("程序等待中...等待网址打开...")
    time.sleep(5)
    try:
        tc = dv.switch_to.alert()
        tc.accept()
        logging.error("系统弹窗点击成功")
    except:
        logging.error("系统弹窗定位失败")
    print("程序等待中...预计需要120秒")
    logging.error("准备签到/签退...等待中...")
    time.sleep(120)  # 公司连北京服务器，会比较慢，这里直接等2min
    try:
        dv.find_element_by_xpath(want_xpath).click()
    except:
        logging.error("签到/签退按钮定位失败,元素值：%s"%(want_xpath))
        dv.close()
        return True
    dv.close()
    return False

def main():
    # open_chorm("")  #第一次调试使用
    # input("输入任意键退出调试程序")

    want_xpaht = calc_time()
    if want_xpaht == "":
        time.sleep(random.randint(30,60))
        return
    else:
        should_again = True
        while should_again:
            should_again = open_chorm(want_xpaht)

while 1:
    today = datetime.now().weekday() + 1
    if today < 6:
        main()
    else:
        time.sleep(3600*24)




