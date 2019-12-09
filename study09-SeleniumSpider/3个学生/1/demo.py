#coding=utf-8

import time
from selenium import webdriver


url = "http://book.zongheng.com/store/c0/c0/b1/u2/p1/v9/s9/t0/u0/i1/ALL.html"

driver = webdriver.Chrome()
driver.get(url)
bookinfolist = []  #定义小说信息列表
def book():
    #循环读取界面中的数据
    for i in range(2):
        try:
            bookinfo = driver.find_elements_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div[2]')
            for i in bookinfo:
                #小说名
                bookname = i.find_element_by_xpath('./div[1]/a').text  
                #小说链接
                bookurl = i.find_element_by_xpath('./div[1]/a').get_attribute('href')  
                #小说类型
                booktype = i.find_element_by_xpath('./div[2]/a[2]').text  
                #小说推荐数量
                bookcount = i.find_element_by_xpath('./div[2]/span[2]').text  
                #小说简介
                bookinstro = i.find_element_by_xpath('./div[3]').text  
                #数据存入小说信息列表
                bookinfolist.append([bookname,booktype,bookcount,bookinstro,bookurl])
             #定位下一页按钮
            driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[3]/div/a[8]').click()
        except:
            print("小说信息加载失败")
        time.sleep(5)
#保存小说数据
def savebook():
    with open('bookinfo','a',encoding="utf-8") as f:
        for i in bookinfolist:
            #按行把数据写入文件中
            f.write(str(i) + '\n') 
    f.close()

#得出结论，打印出排名前10的小说类型
def result():
    for i in range(10):
        print(bookinfolist[i][1])

if __name__ == '__main__':
    #调用读取页面def
    book()
    #调用保存小说数据def
    savebook()
    #调用分析结果def
    result()