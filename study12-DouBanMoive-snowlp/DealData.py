#coding=utf-8

import os

#获取所有文件夹及子文件
def get_all_path(data_file_path):
    rootdir = data_file_path
    path_list = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        com_path = os.path.join(rootdir, list[i])
        if os.path.isfile(com_path):
            #如果文件名是电影评价.txt则获取这个文件的路径
            if com_path.split("\\")[-1] == "电影评价.txt":
                path_list.append(com_path)
        if os.path.isdir(com_path):
            path_list.extend(get_all_path(com_path))
    return path_list

def read_from_txt(file_path):
    content_list = []
    f = open(file_path,"r",encoding="utf-8")
    content_list.append(f.readlines())
    f.close()
    return content_list

def save_to_txt(data):
    f = open("欧美喜剧.txt", "a", encoding="utf-8")
    for i in data:
        for j in i:
            f.write(str(j))
    f.close()


movie_file_list = get_all_path("欧美喜剧")

for i in movie_file_list:
    data = read_from_txt(i)
    save_to_txt(data)
