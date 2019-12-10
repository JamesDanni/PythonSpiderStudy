from selenium import webdriver
import time
import csv
import random

driver = webdriver.Chrome()
driver.maximize_window()
goods_lst = []

def open_jd():
    '''
    打开京东主页，并搜索【卡西欧】
    '''
    try:
        driver.get("https://www.jd.com/")
        time.sleep(1)
        # 定位搜索框，并输入卡西欧
        driver.find_element_by_xpath('//*[@id="key"]').send_keys("卡西欧")
        time.sleep(1)
        # 定位搜索按钮，并点击搜索按钮
        driver.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        time.sleep(1)
    except:
        return

def open_goods():
    '''
    进入卡西欧搜索结果界面，获取商品信息
    '''
    time.sleep(2)
    try:
        js = 'window.scrollTo(0,document.body.scrollHeight)'
        # 滑动浏览器到浏览器底部，以便加载所有商品信息
        driver.execute_script(js)
        time.sleep(2)
        # 根据xpath方法查找页面上的商品信息
        goods_info = driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
        time.sleep(2)
        # 循环读取每一个商品的相关信息
        for i in goods_info:
            #获取当前标签页句柄
            n = driver.window_handles
            #定位标签页
            driver.switch_to.window(n[0])
            time.sleep(3)
            print("get good list NO.%d..."%len(goods_lst))
            # 获取商品名称
            goods_name = i.find_element_by_xpath('./div/div[3]/a/em').text
            # 获取商品价格
            goods_price = i.find_element_by_xpath('./div/div[2]/strong/i').text
            # 获取商品店铺名称
            goods_store = i.find_element_by_xpath('./div/div[5]/span/a').text
            # 获取商品的详情地址
            goods_url = i.find_element_by_xpath('./div/div[1]/a').get_attribute("href")
            # 将商品信息添加到商品信息列表中
            goods_lst.append([goods_name,goods_price,goods_store,goods_url])
            #点击商品，展开商品详情页
            time.sleep(2)
            i.find_element_by_xpath('./div/div[3]/a').click()
            #随机休眠5--10秒，等待页面加载完成
            time.sleep(random.randint(5,10))
            #获取当前页句柄
            n = driver.window_handles
            #切换标签页，切换到新的标签页
            driver.switch_to.window(n[1])
            #定义商品详情列表
            content_info_list = []
            #获取所有商品详情信息
            content_info = driver.find_elements_by_xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li')
            for c in content_info:
                #将每个商品详情信息，添加到商品详情列表中
                content_info_list.append(c.text)
            #保存商品详情信息
            save_content_info(content_info_list)
            driver.close()
            print("关闭商品详情页")
        # 点击下一页，获取下一页的商品数据
        driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]').click()
    except:
        pass

def savegoods():
    #打开文件
    try:
        with open("商品信息.csv","a",newline="",encoding="utf-8") as f:
            a = csv.writer(f)
            for i in goods_lst:
                a.writerow(i)
        f.close()
    except:
        pass

def save_content_info(content_info):
    # 打开文件
    try:
        with open("商品详情.csv", "a", newline="", encoding="utf-8") as f:
            a = csv.writer(f)
            a.writerow(content_info)
        f.close()
    except:
        pass

if __name__ == '__main__':
    open_jd()
    for i in range(20):  #这个20，代表获取20页，循环获取的
        open_goods()
        time.sleep(1)
    savegoods()
    for lst in goods_lst:
        print(lst)