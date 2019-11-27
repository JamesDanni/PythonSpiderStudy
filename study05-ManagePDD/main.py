#coding=utf-8

import requests
import json
import toml
import csv
import time
import logging
import os

def get_page_data(idx):
    '''
    获取店铺列表页面信息
    :param idx:当前页（第几页）
    :return:响应数据
    '''
    url = "http://flyresh.com/admin.php/system/pinduoduo/stores.html?page={}&limit=10".format(idx)
    headers = {
        "Cookie": my_cookie,
        "Referer": "http://flyresh.com/admin.php/system/pinduoduo/stores.html",
        "Host": "flyresh.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Accept": "application / json, text / javascript, * / *; q = 0.01",
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    try:
        ret = requests.get(url, headers=headers, stream=True)
        ret.raise_for_status()
        logging.error("获取店铺列表：%s"%ret.text)
        return ret.text
    except:
        print("获取店铺列表失败！")
        logging.error("获取店铺列表失败！")
        logging.error("获取店铺列表网页源码：%s"%ret.text)
        return None

def deal_page_data(json_str_data):
    '''
    解析响应数据
    :param json_str_data:请求得到的响应数据
    :return:店铺信息列表
    '''
    try:
        data = json.loads(json_str_data)["data"]
    except:
        print("deal_page_data 获取店铺列表失败！")
        logging.error("获取店铺列表失败!")
        logging.error("获取店铺列表结果:%s"%json_str_data)
        return []
    lst = []
    try:
        for i in data:
            d_id = i["id"]                                   #店铺id
            d_name = i["name"]                               #店铺名字
            d_store_remain_total = i["store_remain_total"]   #2--每日限额
            d_status = i["status"]                           #3--状态（0:禁用  1:启用）
            d_set = i["cur_total"]                           #1--成单金额（暂定是nick字段）
            lst.append([d_id,d_name,d_store_remain_total,d_set,d_status])
    except:
        print("获取店铺元素失败！")
        logging.error("获取店铺元素失败,原始数据为:%s"%json_str_data)
        logging.error(data)
    return lst

def save_data(data,idx):
    '''
    保存店铺数据到本地csv文件
    :param data: 店铺数据列表
    :param idx: 循环次数
    :return:
    '''
    if Gidx == 1:  #程序如果第一次运行，则将数据保存到-->预设值.csv
        file_name = Day_Path + "/预设值.csv"
        with open(file_name,"a",newline="",encoding="utf-8") as f:
            f_csv = csv.writer(f)
            if idx == 0:
                f_csv.writerow(["店铺ID","店铺名字","每日限额(2)","成单金额(1)","状态","预设值"])
            for i in data:
                f_csv.writerow(i)
        f.close()
    tmp_file_name = Day_Path + "/时时数据.csv"  #每次运行都更新-->时时数据.csv
    if idx == 0:                               #如果是第一页数据就以覆盖的方式去写文件
        tmp_file = open(tmp_file_name, "w", newline="", encoding="utf-8")
        tmp_csv = csv.writer(tmp_file)
        tmp_csv.writerow(["店铺ID", "店铺名字", "每日限额(2)", "成单金额(1)", "状态"])
        logging.error("店铺列表列名写入时时数据文件成功")
    else:                                      #除了第一页，后续页面都以追加方式写文件
        tmp_file = open(tmp_file_name, "a", newline="", encoding="utf-8")
        tmp_csv = csv.writer(tmp_file)
    for i in data:
        tmp_csv.writerow(i)
    logging.error("店铺列表数据写入时时数据文件成功")
    tmp_file.close()
    return

def get_data_to_csv():
    '''
    爬取店铺信息
    :return:
    '''
    try:
        page_count = json.loads(get_page_data(1))["count"]
    except:
        print("获取店铺列表失败，可能cookie已经过期，请注意核对")
        logging.error("获取店铺列表失败，可能cookie已经过期，请注意核对")
    if page_count % 10 == 0:
        page_count = int(page_count / 10)
    else:
        page_count = int(page_count / 10) + 1
    for i in range(page_count):
        page_data = get_page_data(i+1)
        page_lst = deal_page_data(page_data)
        if len(page_lst) == 0:
            print("店铺列表为空，请注意核对")
            logging.error("店铺列表为空，请注意核对.第%d页的数据"%(i+1))
            continue
        save_data(page_lst,i)

def modify_store_remain_total(d_id,d_store_remain_total):
    '''
    修改店铺每日限额
    :param d_id:店铺ID
    :param d_store_remain_total:修改后的每日限额
    :return:
    '''
    url = "http://flyresh.com/admin.php/system/pinduoduo/stores_remain_total.html"
    headers = {
        "Cookie": my_cookie,
        "Origin":"http://flyresh.com",
        "Referer": "http://flyresh.com/admin.php/system/pinduoduo/stores.html",
        "Host": "flyresh.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    data = {
        "id":d_id,
        "store_remain_total":d_store_remain_total
    }
    try:
        ret = requests.post(url,data = data,headers = headers)
        ret.raise_for_status()
        if json.loads(ret.text)["msg"] == "更新成功":
            print("修改每日限额成功，店铺id:%s" % d_id)
        else:
            print("修改每日限额失败，店铺id:%s" % (d_id))
            logging.error("修改每日限额失败，店铺id:%s 响应数据:%s" % (d_id, ret.text))
    except:
        print("修改每日限额失败，店铺id:%s" % (d_id))
        logging.error("修改每日限额失败，店铺id:%s 响应数据:%s" % (d_id, ret.text))

def modify_status(d_id):
    '''
    修改店铺状态--从停用修改为启用
    :param d_id:店铺ID
    :return:
    '''
    url = "http://flyresh.com/admin.php/system/pinduoduo/stores_status.html"
    headers = {
        "Cookie": my_cookie,
        "Origin": "http://flyresh.com",
        "Referer": "http://flyresh.com/admin.php/system/pinduoduo/stores.html",
        "Host": "flyresh.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    data = {
        "id": d_id,
        "val": 1
    }
    try:
        ret = requests.post(url, data=data, headers=headers)
        ret.raise_for_status()
        if json.loads(ret.text)["msg"] == "更新成功":
            print("修改状态成功，店铺id:%s"%d_id)
        else:
            print("修改状态失败，店铺id:%s"%(d_id))
            logging.error("修改状态失败，店铺id:%s 响应数据:%s"%(d_id,ret.text))
    except:
        print("修改状态失败，店铺id:%s"%(d_id))
        logging.error("修改状态失败，店铺id:%s 响应数据:%s" % (d_id, ret.text))

def compare_data():
    '''
    比较本地数据，判断是否需要修改店铺数据
    :return:
    '''
    file_name = Day_Path + "/预设值.csv"
    tmp_file_path = Day_Path + "/时时数据.csv"
    tmp_csv = csv.reader(open(tmp_file_path,"r",encoding="utf-8"))
    r_csv = csv.reader(open(file_name, "r",encoding="unicode_escape"))
    t_lst = []
    for _t_lst in tmp_csv:
        t_lst.append(_t_lst)
    # ["店铺ID","店铺名字","每日限额(2)","成单金额(1)","状态","预设值"]
    for k,i in enumerate(r_csv):
        logging.error("--------------%d" % k)
        if k == 0:
            continue
        for tk,ti in enumerate(t_lst):
            logging.error("k:%d tk:%d"%(k,tk))
            if tk == k:
                t2,t3,t4 = int(ti[2]),int(ti[3]),int(ti[4])
                logging.error("预设值:%d 成单金额:%d 状态:%d"%(int(i[5]),t3,t4))
                try:
                    c = int(i[5]) - t3
                except:
                    print("数据比对失败~~~~")
                    logging.error("my_set or now_value id null:%d %d"%(i[5],t3))
                    continue
                logging.error("my_set:%d now_value:%d status:%d"%(int(i[5]),t3,t4))
                if c > 1000:
                    if t4 == 0:
                        if t2 > 0:
                            # print("增加2的值")
                            logging.error("需要把店铺：%s 的每日限额修：%d 改成 %d"%(i[0],t2,t2+1000))
                            modify_store_remain_total(i[0],t2 + 1000)
                            time.sleep(3)
                        # print("修改状态为1")
                        modify_status(i[0])
                        time.sleep(time_sleep)
                break

def main():
    logging.error("程序第%d次执行开始"%Gidx)
    get_data_to_csv()
    a = True
    while a:
        if Gidx == 1:  #第一次执行则进行预设值的输入
            Y = input("请前往 %s 文件夹修改文件【预设值.csv】，修改完成后，请输入大写的Y或者小写的y\n"%Day_Path)
            if Y == "Y" or Y == "y":
                logging.error("今日程序已执行%d次，进行本地数据比对中..." % Gidx)
                compare_data()
                a = False
                logging.error("数据比对完毕")
            else:
                print("输入有误，请重新输入")
        else:
            logging.error("今日程序已执行%d次，进行本地数据比对中..." % Gidx)
            compare_data()
            a = False
            logging.error("数据比对完毕")
    print("今日程序第%d次执行完毕" % Gidx)
    print("等待下一次循环...时间%d秒..."%(execsleep))

config = toml.load("config.toml")
my_cookie = config["basic"]["mycookie"]
time_sleep = config["basic"]["timesleep"]
execsleep = config["basic"]["execsleep"]
Day_Path = time.strftime("%Y-%m-%d-%H-%M-%S")
# Day_Path = "2019-11-26-17-05-32"
Gidx = 1  #定义全局变量，表示程序是第一次运行
if not os.path.exists(Day_Path):  # 判断省份文件夹是否存在，不存在就创建一个
    os.makedirs(Day_Path)

logging.basicConfig(level = "ERROR",
                    datefmt = "%Y-%m-%d %H:%M:%S",
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    filename = (Day_Path + "/log.txt"),
                    filemode = 'w'
                    )


while 1:
    main()
    Gidx += 1
    time.sleep(execsleep)

#2019-11-27 17:28