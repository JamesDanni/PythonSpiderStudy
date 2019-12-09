#coding=utf-8

import requests
import logging
import re
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Host":"bbs.pinggu.org",
    "Referer":"https://bbs.pinggu.org/z_index.php?type=2&page=1"
}

def get_content_page(url):
    try:
        ret = requests.get(url,headers = headers)
        return ret.text
    except:
        logging.error("get url:%s fail"%url)
        try:
            logging.error(ret.text)
        except:
            logging.error(ret)
        return ""

def parse_content_page(html_data):
    soup = BeautifulSoup(html_data,"html.parser")
    table_content = soup.find_all(class_ = "post2015")
    user_info = []
    for k,v in enumerate(table_content):
        if k == 0:
            author = re.findall('<strong><a class=\"xi2\".*?>(.*?)</a></strong>',str(v))
            try:
                a = author[0]
                continue
            except:
                logging.error("爬取作者失败了~")
                logging.error(html_data)
                return user_info
        pinglun = re.findall('<strong><a class=\"xi2\".*?>(.*?)</a></strong>',str(v))
        b_pinglun = re.findall('<blockquote><font.*?><font.*?>(.*?) 发表于',str(v))
        try:
            p = pinglun[0]
        except:
            logging.error("评论者为空？")
            continue
        if len(b_pinglun) == 0:
            user_info.append([a,"",p])
            continue
        try:
            user_info.append([a,b_pinglun[0],p])
        except:
            logging.error("parse content page fail!")
            logging.error("作者:%s 被评论者:%s 评论者:%s"%(author,b_pinglun,pinglun))
    return user_info

def get_max_page(html_data):
    soup = BeautifulSoup(html_data,"html.parser")
    try:
        next_url = soup.find("a",class_ = "nxt")["href"]
        return next_url
    except:
        logging.error("爬完一篇帖子了")

