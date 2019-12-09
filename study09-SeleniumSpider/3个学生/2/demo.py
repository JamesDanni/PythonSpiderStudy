#coding=utf-8


import time
from selenium import webdriver
import csv

driver = webdriver.Chrome()
driver.get("https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4")
book_top100 = []  #用于存放所有书籍列表，只存放书名、评分

#在页面上查找数据，并添加到列表中，返回小说信息列表
def find_data():
    data = driver.find_elements_by_xpath('//*[@id="subject_list"]/ul/li')
    book_list = []
    for i in data:
        book_name = i.find_element_by_xpath('./div[2]/h2/a').get_attribute("title")  #书名
        book_mark = i.find_element_by_xpath('./div[2]/div[2]/span[2]').text  #评分
        try:
            book_mark2 = i.find_element_by_xpath('./div[2]/div[3]/div[2]/span[1]/a').text  #纸质版价格
        except:
            book_mark2 = "无纸质版"
        book_assessed_people = i.find_element_by_xpath('./div[2]/div[2]/span[3]').text.replace('(',"").replace('人评价)',"")#评论人数，替换(、人评价)
        book_url = i.find_element_by_xpath('./div[2]/h2/a').get_attribute("href")  #书籍url地址
        book_list.append([book_name,book_mark,book_mark2,book_assessed_people,book_url])  #需要返回的书籍信息列表
        book_top100.append([book_name,book_mark])  #存放所有书籍的书名、评分
    return book_list

# 获取列表的第二个元素
def takeSecond(elem):
    return elem[1]

# 点击下一页
def next_page():
    try:
        driver.find_element_by_xpath('//*[@id="subject_list"]/div[2]/span[4]/a').click()
    except:
        print("打开下一页失败了")

# 保存每一页的数据到文件中
def save_data(book_list):
    c_file = open("数据.csv", 'a', newline="", encoding="utf-8")
    c = csv.writer(c_file)
    for i in book_list:
        c.writerow(i)
    c_file.close()

if __name__ == '__main__':
    for i in range(1):  #获取页数，每页20条数据
        book_list = find_data()
        save_data(book_list)
        time.sleep(3)
        next_page()
    driver.quit()
    print(book_top100.sort(key=takeSecond,reverse=True)[:100])  #对书名、评分列表按评分字段进行降序排列，输出排名前100
