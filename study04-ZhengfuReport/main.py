#coding=utf-8

import requests
from urllib import parse
import re
import time
import os
import random

'''
固定http请求的头部信息
'''
headers = {
        "Referer":'http://data.people.com.cn/pd/gzbg/list.html?qs={%22cId%22:36,%22cds%22:[{%22cdr%22:%22AND%22,%22fld%22:%22class1%22,%22val%22:%22%E5%90%84%E5%9C%B0%E6%94%BF%E5%BA%9C%E5%B7%A5%E4%BD%9C%E6%8A%A5%E5%91%8A%22}]}&id=326&index=9',
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "Cookie":'xxxxxxxx'
    }

'''
定义省份列表
'''
province_lst = ["黑龙江","吉林","辽宁","内蒙古","河北","河南",
                "山东","山西","安徽","江苏","江西","湖北","湖南","浙江","福建","广东","广西",
                "贵州","云南","四川","陕西","甘肃","宁夏","青海","西藏","新疆","海南"]

def get_province_all(province,idx):
    '''
    获取某省份报告，一页20条报告列表
    :param province:省份名称
    :param idx:页数
    :return: 某省份页面数据
    '''
    province = parse.quote(province)
    url = "http://data.people.com.cn/pd/gzbg/list.html?pageNo={}" \
          "&pageSize=20&id=326&isAjax=1&qs=" \
          "%7B%22cId%22%3A%2236%22%2C%22cds%22%3A%5B%7B%22fld%22%3A%22class1%22%2C%22cdr" \
          "%22%3A%22AND%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22" \
          "%3A%22DEF%22%2C%22val%22%3A%22%E5%90%84%E5%9C%B0%E6%94%BF%E5%BA%9C%E5%B7%A5%E4" \
          "%BD%9C%E6%8A%A5%E5%91%8A%22%7D%2C%7B%22cdr%22%3A%22AND%22%2C%22cds%22%3A%5B%7B" \
          "%22fld%22%3A%22class2%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22false%22%2C%22" \
          "vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%22" \
          "{}" \
          "%22%7D%5D%7D%5D%2C" \
          "%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D".format(idx,province)
    try:
        ret = requests.get(url, headers=headers)  #发送请求
        ret.raise_for_status()   #判断http请求状态码是否为200
        return ret.text
    except:
        print("get_province_all {} Fail,Page:{}".format(province,idx))
        return None

def get_report_data(province,url):
    '''
    获取某一具体报告的内容
    :param province: 省份名称（在获取数据发生错误时可以打印）
    :param url: 某一条报告的url参数
    :return: 具体报告的页面内容
    '''
    url = "http://data.people.com.cn" + url  #url参数拼接
    try:
        ret = requests.get(url,headers = headers)
        ret.raise_for_status()
        return ret.text
    except:
        print("get_report_data {} Fail,url:{}".format(province,url))
        return None

def get_max_idx(data,addr):
    '''
    解析某个省份下共几页报告列表
    :param data: 某个省份下的网页源码
    :return: 返回共几页
    '''
    pattern_idx = re.compile('共   (\d*)   页', re.S)
    try:
        idx = re.findall(pattern_idx, data)[0]  #获取页数失败就抛出异常
    except:
        print("get %s page fail"%addr)
        print(data)
        return 1
    return int(idx)

def paras_province_data(addr,page,data):
    '''
    解析某一省份下的一页报告列表
    :param data: 报告列表网页源码
    :return: url地址列表
    '''
    page_url_lst= []  #定义一个空列表，用于后面存放某个省份--某一页的所有报告的url
    tmp_pattern_url = re.compile('<ul class="list_ul clearfix">(.*?)</ul>', re.S)
    tmp_url_lst = re.findall(tmp_pattern_url, data)
    pattern_url = re.compile('href=\"(.*?)\"', re.S)
    try:
        url_lst = re.findall(pattern_url, tmp_url_lst[0])   #如果网页源码中的报告列表为空，则抛出一个异常
    except:
        print("paras_province_data fail:%s page:%d"%(addr,page))
        return page_url_lst
    for url in url_lst:  #url列表迭代
        page_url_lst.append(url)
    return page_url_lst

def paras_report_data(data,addr,page):
    '''
    解析具体某一个报告内容
    :param data:具体报告页面的所有内容
    :return: 提取出来的具体报告内容
    '''
    pattern_h2 = re.compile('<h2>(.*?)</h2>', re.S)
    try:
        report_title = re.findall(pattern_h2, data)[0]  #获取报告标题
    except:  #获取不到报告标题，将报告标题置为空
        report_title = addr + "_" + str(page) + "_未获取成功"
    tmp_pattern_content = re.compile('<div class=\"detail\" id=\"jqprint\">(.*?)<div id=\"saveArticleModal', re.S)
    tmp_report_content = re.findall(tmp_pattern_content, data)  #获取报告正文内容（临时字段）
    pattern_content = re.compile('<p>(.*?)</p>', re.S)
    try:
        report_content = re.findall(pattern_content, tmp_report_content[0])
    except:  #如果获取不到报告正文内容，抛出异常，正文内容为空
        print("报告正文内容为空，请注意核对! 省份%s 页数:%d"%(addr,page))
        report_content = ""
    report_data = report_title + "\n"
    for content in report_content:   #解析报告正文内容，每段之间输入一个回车
        report_data = report_data + content + "\n"
    return report_title, report_data

def save_file(file_path,file_name,data):
    '''
    把报告保存到指定目录下的指定文件中
    :param file_path: 报告存放的路径
    :param file_name: 报告文件名
    :param data: 报告内容
    '''
    if not os.path.exists(file_path):  #判断省份文件夹是否存在，不存在就创建一个
        os.makedirs(file_path)
    file_name = file_path + "/" + file_name + ".txt"
    with open(file_name,"w",encoding='utf-8') as f:
        try:
            f.write(data)
        except:
            print("请注意 %s 文件夹下的 %s文件编码存在问题，请注意核对"%(file_path,file_name))
    f.close()

def main():
    for addr in province_lst:  #循环取每个省份
        tmp_data = get_province_all(addr,1)
        idx = get_max_idx(tmp_data,addr)
        time.sleep(1)
        for idx in range(1,idx+1):  #循环取某个省份下，所有页面，idx表示一共几页
            province_data = get_province_all(addr,idx)
            url_list = paras_province_data(addr,idx,province_data)
            time.sleep(1)
            for url in url_list:   #循环取某个省份下 某个页面(20条数据)的具体报告
                report_data = get_report_data(addr,url)
                report_title,report_content = paras_report_data(report_data,addr,idx)
                save_file(addr,report_title,report_content)
                time.sleep(random.randint(10,20))

main()
