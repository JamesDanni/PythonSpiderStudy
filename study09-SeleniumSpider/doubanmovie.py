#coding=utf-8

from time import sleep as s
from urllib import parse
from selenium import webdriver
import csv

class DouBan():
    def __init__(self,page_count):
        self.dv = webdriver.Chrome()
        self.page_count = page_count  #点击加载更多的次数
        self.data = []

    #获取页面信息
    def get_page_data(self,name):
        type_name = parse.quote(name)
        url = "https://movie.douban.com/tv/#!type=tv&tag={}&sort=recommend&page_limit=20&page_start=20".format(type_name)
        self.dv.get(url)
        s(3)
        for i in range(self.page_count):
            print(name)
            h = self.dv.find_element_by_partial_link_text('加载更多')
            h.click()
            s(5)
        #获取页面cotent
        movie_list = self.dv.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div/div[4]/div/a')
        for i in range(1,len(movie_list)+1):
            name_path = '//*[@id="content"]/div/div[1]/div/div[4]/div/a[{}]/div/img'.format(i)
            result_path = '//*[@id="content"]/div/div[1]/div/div[4]/div/a[{}]/p/strong'.format(i)
            movie_name = self.dv.find_element_by_xpath(name_path).get_attribute("alt")
            if len(movie_name) == 0:
                continue
            movie_result = self.dv.find_element_by_xpath(result_path).text
            if len(movie_result) == 0:
                continue
            self.data.append([movie_name,str(movie_result)])

    #保存数据
    def save_data(self,name):
        file_name = name + "数据" + ".csv"
        c_file = open(file_name,'w',newline="",encoding="utf-8-sig")
        f = csv.writer(c_file)
        f.writerow(["名称","评分"])
        for i in self.data:
            f.writerow(i)

    def exit_chorm(self):
        self.dv.close()

if __name__ == '__main__':
    type_name = ["热门","美剧","英剧","韩剧"]  #类别列表
    page_count = 1  #每个类别爬取几页
    for name in type_name:
        _spider = DouBan(page_count)
        _spider.get_page_data(name)
        _spider.save_data(name)
        _spider.exit_chorm()
        s(10)