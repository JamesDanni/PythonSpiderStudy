#coding=utf-8

import requests
import re
# from . import IndexPage,Content,SaveData
import IndexPage,Content,SaveData
import logging

logging.basicConfig(level = "ERROR",
                    datefmt = "%Y-%m-%d %H:%M:%S",
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    filename = "log.txt",
                    filemode = 'w'
                    )

def main():
    page_idx = 50
    for i in range(page_idx):
        index_page_data = IndexPage.get_index_page(1)  #获取30天热门，网页内容（一页20条帖子）
        if index_page_data == "":
            continue
        url_info = IndexPage.parse_index_page(index_page_data)  #获取一页帖子的所有url
        for url in url_info:
            next_url = url
            while next_url:
                content_page_data = Content.get_content_page(next_url)
                next_url = Content.get_max_page(content_page_data)
                if content_page_data == "":
                    logging.error("获取帖子详情页失败,帖子url:%s"%url)
                    continue
                else:
                    user_info = Content.parse_content_page(content_page_data)
                    if user_info == []:
                        logging.error("获取用户评论关系失败了，直接下一页吧")
                        continue
                    else:
                        SaveData.save_data(user_info)


if __name__ == '__main__':
    main()