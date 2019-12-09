#coding=utf-8

import csv

def save_data(data_list):
    f = open("数据.csv","a",newline="",encoding="utf-8")
    c = csv.writer(f)
    for i in data_list:
        c.writerow(i)
    f.close()