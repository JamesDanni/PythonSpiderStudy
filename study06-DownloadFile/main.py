#coding=utf-8

import requests
import re
from threading import Thread
import logging

logging.basicConfig(level = "ERROR",
                    datefmt = "%Y-%m-%d %H:%M:%S",
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    filename = ("log.txt"),
                    filemode = 'w'
                    )

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}

def get_page():
    url = "http://data.ess.tsinghua.edu.cn/fromglc10_2017v01.html"
    ret = requests.get(url,headers = headers)
    tmp_pattern = re.compile('</tr>(.*)</table>',re.S)
    tmp_data = re.findall(tmp_pattern,ret.text)
    pattern = re.compile('<td>(.*?)</td><td><a.*?\"(.*?)\">',re.S)
    lst = re.findall(pattern,str(tmp_data))
    return lst

def download_data(filename,url):
    f_name = Fpath + filename
    try:
        ret = requests.get(url,headers)
    except:
        logging.error("下载失败:%s URL:%s"%(filename,url))
        return
    try:
        _file = open(f_name,"wb")
        _file.write(ret.content)
    except:
        logging.error("保存失败:%s URL:%s"%(filename,url))

def main():
    if TH:
        for i in range(len(page_data)):
            th = Thread(target=download_data,args=(page_data[i][0],page_data[i][1]))
            th_lst.append(th)
        for i in th_lst:
            i.start()
        for i in th_lst:
            i.join()
    else:
        for i in page_data:
            filename = i[0]
            url = i[1]
            download_data(filename,url)

page_data = get_page()
Fpath = "MyDownload/"
TH = False
th_lst = []
main()