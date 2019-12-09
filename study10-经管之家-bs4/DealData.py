#coding=utf-8

import csv
import logging
from collections import Counter

logging.basicConfig(level = "ERROR",
                    datefmt = "%Y-%m-%d %H:%M:%S",
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    filename = "log.txt",
                    filemode = 'w'
                    )

def read_data_from_csv():
    f = open("数据.csv","r",encoding="utf-8")
    c = csv.reader(f)
    all_user = []  #所有评论者
    all_b_user= []  #所有被评论者
    for i in c:
        all_user.append(i[2])
        all_b_user.append(i[1])
    return all_user,all_b_user

def save_data_to_csv(data):
    f = open("最终结果.csv","a",encoding="utf-8",newline="")
    c = csv.writer(f)
    # for i in data:
    c.writerow(data)
    f.close()

all_user_list,all_b_user_list = read_data_from_csv()
# print(all_user_list)
# print(all_b_user_list)
count_user = Counter(all_user_list)  #对所有用户出现次数进行统计
# print(count_user)
# print(len(count_user))
# print("\n\n\n\n\n\n")
d = sorted(count_user.items(), key=lambda x: x[1], reverse=True)  #对统计次数进行排序，降序
# print(d)  #格式为[('user1',count),('user2',count)]
top_100_user = []
tmp_top_100_user = []
for i in range(100):
    top_100_user.append(d[i][0])
# print(top_100_user)
tmp_top_100_user = top_100_user
title_save = []
title_save.append("")
for i in top_100_user:
    title_save.append(i)
save_data_to_csv(title_save)
# print(tmp_top_100_user)
for t in top_100_user:  #遍历前100个用户
    Tag_Value = 0
    a_list = []
    save_list = []
    a_list.append([t])
    for tmp in tmp_top_100_user:  #遍历 t 用户与前100个用户的对应关系，等t遍历到100时，便形成100*100的矩阵
        t_list = []
        if i == tmp:  #如果t跟tmp相等，说明是同一个用户，直接返回，进入下一次遍历
            t_list.append(0)
        else:
            for i in range(len(all_user_list)):  #遍历所有用户关系
                if all_user_list[i] == t and all_b_user_list[i] == tmp:  #评论者是t，被评论者是tmp，那么把1加入列表
                    t_list.append(1)
                    break
                else:
                    continue
        if len(t_list) == 0:
            t_list.append(0)
        a_list.append(t_list)
    # logging.error("%s" % (a_list))

    for sa in a_list:
        save_list.append(sa[0])
    logging.error(save_list)
    save_data_to_csv(save_list)





