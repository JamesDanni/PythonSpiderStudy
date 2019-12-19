#coding=utf-8

import requests
import json
from urllib import parse

def get_doubanmovie_index(movie_type,idx,headers):
    '''
    获取电影类别页面内容
    :param movie_type:电影类别
    :param headers:请求头部信息
    :return:电影类别页面数据
    '''
    page_idx = idx * 180
    _movie_type = parse.quote(movie_type)  #将中文进行url编码
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag={}&sort=recommend&page_limit=20&page_start={}".format(_movie_type,page_idx)
    try:
        ret = requests.get(url,headers=headers)
        ret.raise_for_status()  #判断http头中的状态码是否为200
    except:
        print("获取电影:%s 页面内容出错"%movie_type)
        return ""
    return ret.text

def get_movie_list(data):
    '''
    解析电影页面数据，主要为了获取电影名称及电影详情页url
    :param data:电影类别页面数据
    :return:电影名称及电影详情页url
    '''
    movie_list = []
    try:
        tmp_data = json.loads(data)
        subjects_data = tmp_data["subjects"]
        for i in subjects_data:
            movice_name = i["title"]
            movie_url = i["url"]
            movie_list.append([movice_name,movie_url])
    except:
        print("获取电影名称及电影详情页失败~")
    return movie_list
