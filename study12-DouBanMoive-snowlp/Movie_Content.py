#coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import time

def movie_content_page(url,headers):
    '''
    获取电影详情页内容
    :param url:电影详情页url
    :param headers:请求头
    :return:电影详情页数据
    '''
    try:
        ret = requests.get(url,headers = headers)
        ret.raise_for_status()
    except:
        print("获取电影详情页失败,url:%s"%url)
        return ""
    return ret.text

def handle_movie_data(data):
    '''
    解析电影详情页数据，提取演员表、剧情介绍
    :param data:电影详情页所有数据
    :return:电影演员表
    :return:电影剧情介绍
    '''
    #演员数据
    actor_list = []
    tmp_pattern_actor = re.compile('class=\"actor\">(.*?)<br/>')
    tmp_actor = re.findall(tmp_pattern_actor,data)
    pattern_actor = re.compile('<a.*?>(.*?)</a>')
    actor = re.findall(pattern_actor,str(tmp_actor))
    for a in actor:
        actor_list.append([a,""])

    #剧情简介
    movie_type = re.findall('property=\"v:genre\">(.*?)</span>', data)
    movie_content_pattern = re.compile('\u3000\u3000(.*?)\u3000\u3000', re.S)
    movie_content = re.findall(movie_content_pattern,data)
    if len(movie_content) == 0:
        movie_content_pattern = re.compile('v:summary.*?>(.*?)</span>', re.S)
        movie_content = re.findall(movie_content_pattern, data)

    #评价
    soup = BeautifulSoup(data,"html.parser")
    appraise_list = soup.find_all("div",class_ = "short-content")
    appraise_list_content = []
    for i in appraise_list:
        save_data = (i.get_text())
        save_data = (''.join(save_data.split())).replace('(展开)','').replace('.','').replace('这篇影评可能有剧透','') + '\n'
        appraise_list_content.append(save_data)
    return actor_list,movie_content,movie_type,appraise_list_content