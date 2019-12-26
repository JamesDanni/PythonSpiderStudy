#coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import time

class MovieContent():
    def movie_content_page(self,url,headers):
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

    def handle_movie_data(self,data):
        '''
        解析电影详情页数据，提取演员表、剧情介绍
        :param data:电影详情页所有数据
        :return:电影演员表
        :return:电影剧情介绍
        '''
        #评价
        soup = BeautifulSoup(data,"html.parser")
        appraise_list = soup.find_all("div",class_ = "short-content")
        appraise_list_content = []
        for i in appraise_list:
            save_data = (i.get_text())
            save_data = (''.join(save_data.split())).replace('(展开)','').replace('.','').replace('这篇影评可能有剧透','')
            appraise_list_content.append(save_data)
        # return actor_list,movie_content,movie_type,appraise_list_content
        return appraise_list_content