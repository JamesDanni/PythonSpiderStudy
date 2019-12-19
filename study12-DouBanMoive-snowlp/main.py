#coding=utf-8

import time
import os
import Movie_Index
import Movie_Content
import Save_Data

my_cookie = 'bid=XSlOA6ZeRpc; __utmz=30149280.1575194025.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmz=223695111.1575194025.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=rPZIwJzjKugN7TlpM5XL4XJZW4MODW8b; ll="118172"; trc_cookie_storage=taboola%2520global%253Auser-id%3D2ade0f63-35e0-422b-bf79-ebbcfc765223-tuct4dd2e31; _vwo_uuid_v2=D579A0DF2585E15EBFB5041E50B7CB934|4f1481cdfd9c6076c3cf01c47fc21fd6; ap_v=0,6.0; _pk_id.100001.4cf6=6c32cf30dbeaaf7b.1575194025.11.1576395042.1576392902.; _pk_ses.100001.4cf6=*; __utma=30149280.264732620.1575194025.1576392903.1576395042.11; __utmb=30149280.0.10.1576395042; __utmc=30149280; __utma=223695111.639305356.1575194025.1576392903.1576395042.11; __utmb=223695111.0.10.1576395042; __utmc=223695111'
headers = {
    "Referer":"https://movie.douban.com/explore",
    # "Cookie":my_cookie,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}

def main(movie_type,count):
    mk_path = '数据集' + "\\" + movie_type
    if not os.path.exists(mk_path):  #类别文件夹如果不存在，就创建
        os.makedirs(mk_path)
    for idx in range(count):
        index_data = Movie_Index.get_doubanmovie_index(movie_type,idx,headers)  #获取该类别的电影主页内容
        movie_url_list = Movie_Index.get_movie_list(index_data)     #解析该主页内容，得到["电影名称","电影详情页url"]
        time.sleep(3)
        for url_list in movie_url_list:
            movie_name = url_list[0]
            movie_url = url_list[1]
            movie_file_path = mk_path + "\\" + movie_name  #电影名称的文件夹路径
            if not os.path.exists(movie_file_path):        #判断电影名称的文件夹是否存在，不存在则创建
                os.makedirs(movie_file_path)
            movie_content_data = Movie_Content.movie_content_page(movie_url, headers)  #获取电影详情页的内容
            actor,content,type_list,movie_appraise = Movie_Content.handle_movie_data(movie_content_data)  #获取电影演员表及剧情介绍
            Save_Data.save_actor(movie_file_path,actor)    #保存电影演员表
            Save_Data.save_content(movie_file_path,content)  #保存电影剧情介绍
            Save_Data.save_type(movie_file_path,type_list)
            Save_Data.save_appraise(movie_file_path,movie_appraise)
            print("已爬取一部电影")
            time.sleep(5)

if __name__ == '__main__':
    if not os.path.exists('数据集'):
        os.mkdir('数据集')
    want_get_movie = ["华语","欧美"]  #定义需要爬取的类别列表
    COUNT = 10  #定义爬取页数，每页20条
    for type_name in want_get_movie: #遍历需要爬取的类别列表
        main(type_name,COUNT)
        time.sleep(3)
