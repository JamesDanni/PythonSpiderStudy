#codingutf-8

import requests
import re
from sqlserver import *
from urllib import parse
from bs4 import BeautifulSoup

def get_baidu_page(idx):
    '''
    模拟百度搜索请求
    :param idx:页数
    :return:获取到的页面源码
    '''
    # 百度搜索的关键词
    x_name = "徐念沙"
    # 对关键词进行url编码
    name = parse.quote(x_name)
    url = "https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd={}&medium=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.488885&tngroupname=organic_news&rsv_dl=news_b_pn&pn={}".format(name,idx*10)
    # 构造请求头，模拟浏览器去访问网站
    headers = {
        "Referer":"https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%E5%BE%90%E5%BF%B5%E6%B2%99",
        "Host":"www.baidu.com",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    # 发送GET请求
    ret = requests.get(url,headers = headers)
    return ret.text

def parse_baidu_data(html_data):
    '''
    解析百度页面源码
    :param html_data:页面源码数据
    :return:返回需要的数据信息
    '''
    # 使用bs4框架解析网页源码
    soup = BeautifulSoup(html_data,"html.parser")
    get_url = soup.find_all("div",class_ = "result")
    # 定义提取结果数据列表
    result_data = []
    for i in get_url:
        # 用正则表达式获取新闻的url
        url = re.findall('href=\"(.*?)\"',str(i))[0]
        # 用正则表达式提取新闻摘要
        tmp_content = re.findall('</p>\\s*(.*?)\\s*<span',str(i))
        # 对新闻摘要进行数据处理，替换<em>、...等数据
        content = tmp_content[0].replace("<em>",'').replace("</em>",'').replace("...","")
        # 提取新闻发布时间
        tmp_date_time = i.find('p').get_text()
        date_time = re.findall('\d.*?:\d\d',tmp_date_time)[0]
        # 提取新闻标题
        title = i.find("h3",class_ = "c-title").find("a").get_text().strip()
        # 将提取结果存入数据列表中
        result_data.append([title,date_time,content,url])
    return result_data

def get_poly_data(idx):
    '''
    访问保利新闻动态网页，获取网页源码
    :param idx: 新闻动态标签
    :return: 网页源码
    '''
    # 新闻动态页面url
    url = "http://www.poly.com.cn/{}.html".format(idx)
    # 构造请求头，模拟浏览器去访问网站
    headers = {
        "Host": "www.poly.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    ret = requests.get(url,headers = headers)
    return ret.text

def parse_poly_data(html_data):
    '''
    解析网页源码
    :param html_data: 获取到的网页源码
    :return: 提取到的数据
    '''
    soup = BeautifulSoup(html_data,"html.parser")
    tmp_data = soup.find_all("div",class_ = "news-lb-item")
    # 定义提取的数据结果列表
    result = []
    for i in tmp_data:
        # 提取标题
        title = i.find("a")["title"]
        # 提取url
        url = i.find("a")["href"]
        # 提取时间
        date_time = i.find("div",class_ = "news-lb-item-date").find("p").get_text() + "-" + i.find("div",class_ = "news-lb-item-date").find("b").get_text()
        result.append([title,date_time,url])
    return result

def get_content_page(url):
    '''
    获取新闻具体内容
    :param url: 新闻具体内容的url
    :return: 新闻具体内容页面源码
    '''
    # 请求头
    headers = {
        "Host": "www.poly.com.cn",
        "Referer":url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    ret = requests.get(url,headers = headers)
    return ret.text


def save_images(data,image_name):
    '''
    保存图片
    :param data:图片数据
    :param image_name:图片名称
    :return:
    '''
    # 打开图片文件夹下的文件
    f = open("图片/" + image_name,"wb")
    # 保存图片
    f.write(data)
    # 关闭文件
    f.close()

def parse_content_page(data):
    '''
    解析具体内容页面
    :param data:具体内容页面源码
    :return:新闻具体内容
    '''
    soup = BeautifulSoup(data,"html.parser")
    tmp_content = soup.find("div",id = "Content").find_all("p")
    content = ""
    for i in tmp_content:
        image_url = ""
        try:
            # 提取图片的url
            image_url = i.find("img")["src"]
        except:
            # 如果不是图片的数据，则将数据作为新闻的内容保存下来
            content = content + i.get_text() + "\n"
        # 图片的url不为空时，去下载该图片资源
        if image_url != "":
            image_name = image_url.split("/")[-1]
            image_url = "http://www.poly.com.cn" + image_url
            ret = requests.get(image_url)
            # 将图片资源保存到本地
            save_images(ret.content, image_name)
    return content

if __name__ == '__main__':
    # 获取百度的“徐念沙”搜索结果
    print("获取百度徐念沙新闻数据...")
    # 连接数据库
    create_baidutable_data()
    for idx in range(3):
        data = get_baidu_page(idx)
        need_save = parse_baidu_data(data)
        insertinto_baidutable(need_save)
    print("百度数据获取结束,且保存成功...")

    # 获取保利网站的数据集
    print("开始获取poly数据...")
    create_polytable_data()
    need_get_poly = [1089,1076,1090,1091,1092,1094]  #依次代表 领导动态、集团新闻、下属企业动态、国资动态、集团公告、媒体聚焦
    # 依次获取每个标签的内容
    for page in need_get_poly:
        data = get_poly_data(page)
        tmp_list = parse_poly_data(data)  #这里返回的是标题、时间、url
        # 依次获取每个新闻的具体页面内容，并解析提取数据
        for i in tmp_list:
            content_data = get_content_page(i[2])  #获取url，并向该url发起请求
            result_str= parse_content_page(content_data)  #这里返回的是具体内容
            # 如果正文长度超过700，则只取前700
            if len(result_str) > 700:
                result_str = result_str[:700]
            # 拼接所需的新闻数据
            save_list = [i[0],i[1],result_str,i[2]]
            # 将所需的新闻数据保存到数据库中
            insertinto_polytable(save_list)