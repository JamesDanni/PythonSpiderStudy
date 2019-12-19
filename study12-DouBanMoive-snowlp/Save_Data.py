#coding=utf-8

import csv

def save_actor(file_path,data):
    '''
    保存电影演员信息
    :param file_path:保存的路径信息
    :param data: 电影演员信息
    :return:
    '''
    file_name = file_path + "\\" + "演员表.csv"  #在电影名的文件夹下，将数据保存到演员表.csv
    o_file = open(file_name,"w",newline="",encoding="utf-8-sig")
    f = csv.writer(o_file)
    for i in data:
        f.writerow(i)
    o_file.close()

def save_content(file_path,data):
    '''
    保存电影剧情介绍信息
    :param file_path: 保存的路径信息
    :param data: 电影剧情介绍
    :return:
    '''
    try:
        tmp_data = data[0]
    except:
        print("%s电影剧情介绍保存失败"%file_path)
    file_name = file_path + "\\" + "剧情介绍.txt"
    f = open(file_name, "w", encoding="utf-8-sig")
    f.write(str(tmp_data).encode("utf-8").decode("utf-8"))
    f.close()

def save_type(file_path,data):
    '''
    保存电影剧情介绍信息
    :param file_path: 保存的路径信息
    :param data: 电影剧情介绍
    :return:
    '''
    file_name = file_path + "\\" + "电影类型.txt"
    f = open(file_name, "w", encoding="utf-8-sig")
    for i in data:
        f.write(str(i).encode("utf-8").decode("utf-8"))
    f.close()

def save_appraise(file_path,data):
    file_name = file_path + "\\" + "电影评价.txt"
    f = open(file_name,"a",encoding="utf-8")
    for i in data:
        f.write(str(i))
    f.close()