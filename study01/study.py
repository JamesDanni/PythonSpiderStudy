#coding=utf-8

import requests
from bs4 import BeautifulSoup
import csv

#获取网页信息
def db():
    url = "https://www.douban.com/group/"
    headers = {
        "User-Agent":"Mozilla/5.0",
        "Cookie":'xxxxxxx'    #cookie从网页中获取
    }
    ret = requests.get(url,headers = headers)
    ret.encoding = ret.apparent_encoding
    return ret.content

#解析网页，并获取帖子的url、标题
def get_data(lst,html_data):
    soup = BeautifulSoup(html_data,"html.parser")
    for i in soup.find_all("a",attrs="title"):
        lst.append([i.attrs["href"],i.attrs["title"]])

#保存url、标题到csv文件中
def save_to_csv(lst):
    with open('test.csv','w',newline='',encoding='utf-8')as f:
        f_csv = csv.writer(f)
        for data in lst:
            f_csv.writerow(data)

def main():
    Html = db()
    lst = []
    get_data(lst,Html)
    save_to_csv(lst)

main()
