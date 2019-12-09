#coding=utf-8

import requests
import logging
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Host":"bbs.pinggu.org"
}

def get_index_page(idx):
    url = "https://bbs.pinggu.org/z_index.php?type=2&page={}".format(idx)
    headers["Referer"] = url
    try:
        ret = requests.get(url,headers = headers)
        return ret.text
    except:
        logging.error("获取页面失败,下一页吧")
        try:
            logging.error(ret.text)
        except:
            logging.error(ret)
        return ""

def parse_index_page(html_data):
    soup = BeautifulSoup(html_data,"html.parser")
    url_list = []
    info_list = soup.find_all(attrs = {"title": "新窗口中打开"})   #获取属性值为"新窗口中打开"
    for i in info_list:
        url_list.append(i["href"])  #获取info_list中herf属性的值
    return url_list


