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
    '''
    获取网页中的内容，并提取文件名、下载地址
    :return:返回[["文件名1","下载地址1"],["文件名2","下载地址2"],...]
    '''
    url = "http://data.ess.tsinghua.edu.cn/fromglc10_2017v01.html"
    ret = requests.get(url,headers = headers)
    tmp_pattern = re.compile('</tr>(.*)</table>',re.S)
    tmp_data = re.findall(tmp_pattern,ret.text)
    pattern = re.compile('<td>(.*?)</td><td><a.*?\"(.*?)\">',re.S)
    lst = re.findall(pattern,str(tmp_data))
    return lst

def download_data(filename,url):
    '''
    下载文件
    :param filename: 文件名称
    :param url: 下载地址
    :return:
    '''
    f_name = Fpath + filename
    try:
        ret = requests.get(url,headers)
    except:
        logging.error("下载失败:%s URL:%s"%(filename,url))
        return
    try:
        _file = open(f_name,"wb")
        _file.write(ret.content)
        _file.close()
    except:
        logging.error("保存失败:%s URL:%s"%(filename,url))

def main():
    Gidx = 0
    if TH:  #如果是同时下载多个文件
        for i in range(len(page_data)):  #装载线程
            th = Thread(target=download_data,args=(page_data[i][0],page_data[i][1]))
            th_lst.append(th)
        for idx in range(download_th):   #按组别执行线程（每组download_th个同时下载）
            end_idx = Gidx + download_th
            if end_idx > len(page_data):
                end_idx = len(page_data)
            for i in th_lst[Gidx:end_idx]:  #启动线程
                i.start()
            for i in th_lst[Gidx:end_idx]:  #等待线程执行结束
                i.join()
            Gidx += download_th             #控制当前已执行几个线程
    else:  #单个下载
        for i in page_data:
            filename = i[0]
            url = i[1]
            download_data(filename,url)

page_data = get_page()
Fpath = "MyDownload/"
TH = False        #是否启用同时下载多个文件
download_th = 10  #如果TH为True，则此参数表示同时下载的数据量
th_lst = []
main()
