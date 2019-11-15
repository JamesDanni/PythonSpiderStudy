#coding=utf-8

import requests
# from bs4 import BeautifulSoup
import csv
import re

def get_html(url,idx):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64)",
        "Referer":"http://www.qiangmi.com/guoqiyumingchaxun.html",  #该网站对header referer有校验
        "Cookie":'xxxxxxxx'  #cookie请自行获取
    }
    data = {
        "pageIndex":idx,
        "pageCount":50,
        "action":"",
        "position":1,
        "unposition":1,
        "doublep":0,
        "regyear":0,
        "ptype":"",
        "day":0,
        "actiontime":-1,
        "beiandiqu":0,
        "beianxingzhi":0,
        "ddlclass":0,
        "ddltypes":-1,
        "morepr":0,
        "morequanzhong":0,
        "show":"undefined",
        "strlen":"1,200",
        "orderby":"num_d",
        "chaxunkey":"xxxx"  #query key请自行获取
    }
    ret = requests.post(url,data = data,headers = headers)
    return ret.content

def paras_data(data):
    lst = []
    tmp_data = str(data)
    domain = re.findall(r'\"Domain\":\".*?\"',tmp_data)
    delflag = re.findall(r'\"Deltype\":\".*?\"',tmp_data)
    for i in range(len(delflag)):
        if eval(delflag[i].split(":")[1]) == "Delete":
            lst.append([eval(domain[i].split(":")[1]),eval(delflag[i].split(":")[1])])
    return lst

def save_to_file(lst):
    with open("test.csv","a+",newline='',encoding='utf-8') as f:  #循环写文件，所以需要以a形式打开,w是覆盖方式
        f_csv =  csv.writer(f)
        for i in lst:
            f_csv.writerow(i)
        f.close()

def main():
    url = "http://www.qiangmi.com/ajax/order/chaxun.ashx?t=0.9846745977537313"
    for i in range(10344,10355):
        lst = paras_data(get_html(url,i))
        save_to_file(lst)

main()
