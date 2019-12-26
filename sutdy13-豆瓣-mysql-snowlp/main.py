#coding=utf-8

import time
from Movie_Index import MovieIndex
from Movie_Content import MovieContent
from Save_Mysql import SaveToMysql
from Nlp import DataVisual

headers = {
    "Referer":"https://movie.douban.com/explore",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}

def main(movie_type,count):
    s = SaveToMysql('192.168.77.129', 'root', '123456', 'mydb', 'mymoviedata')
    s.create_table()
    m_index = MovieIndex()
    m_content = MovieContent()
    d = DataVisual()
    for idx in range(count):
        index_data = m_index.get_doubanmovie_index(movie_type,idx,headers)  #获取该类别的电影主页内容
        movie_url_list = m_index.get_movie_list(index_data)     #解析该主页内容，得到["电影名称","电影详情页url"]
        time.sleep(3)
        for url_list in movie_url_list:
            save_data = []
            movie_name = url_list[0]
            movie_url = url_list[1]
            movie_content_data = m_content.movie_content_page(movie_url, headers)  #获取电影详情页的内容
            movie_appraise = m_content.handle_movie_data(movie_content_data)
            for remark in movie_appraise:
                save_data.append((movie_name,remark,movie_url))
            s.insert_data(save_data)
            print("第%d页，已爬取一部电影"%idx)
            time.sleep(5)
        print("爬取第%d页数据完毕"%idx)
    print("已经爬取完毕，开始数据分析并绘图")
    ret = s.select_data()
    d.visual(movie_type,ret)
    print("绘图完毕！")


if __name__ == '__main__':
    want_get_movie = ["华语"]  #定义需要爬取的类别列表
    COUNT = 2  #定义爬取页数，每页20条
    for type_name in want_get_movie: #遍历需要爬取的类别列表
        main(type_name,COUNT)
        time.sleep(3)


