#coding=utf-8

import requests
import json
import toml
import csv
import time
import logging

logging.basicConfig(level = "ERROR",
                    datefmt = "%Y-%m-%d %H:%M:%S",
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    filename = "log.txt",
                    filemode = 'w'
                    )

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
            d_set = i["nick"]                                #1--成单金额（暂定是nick字段）TODO
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
    file_path = time.strftime("%Y-%m-%d")
    file_name = file_path + ".csv"
    with open(file_name,"a",newline="",encoding="utf-8") as f:
        f_csv = csv.writer(f)
        if idx == 0:
            f_csv.writerow(["店铺ID","店铺名字","每日限额(2)","成单金额(1)","状态","预设值"])
        for i in data:
            f_csv.writerow(i)
    f.close()

def get_data_to_csv():
    '''
    爬取店铺信息
    :return:
    '''
    try:
        page_count = json.loads(get_page_data(1))["count"]
    except:
        print("获取店铺列表失败")
        logging.error("获取店铺列表失败")
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
    file_path = time.strftime("%Y-%m-%d")
    file_name = file_path + ".csv"
    r_csv = csv.reader(open(file_name, "r",encoding="unicode_escape"))
    # ["店铺ID","店铺名字","每日限额(2)","成单金额(1)","状态","预设值"]
    for k,i in enumerate(r_csv):
        if k == 0:
            continue
        try:
            if i[5] == "" or i[3] == "":
                continue
            c = int(i[5]) - int(i[3])
        except:
            print("csv的第%d行预设值为空?，默认应该是0"%(k+1))
            logging.error("csv的第%d行预设值为空?，默认应该是0,获取到的数据为:%s"%(k+1,i))
            continue
        if c > 1000:
            if int(i[4]) == 0:
                #print("增加2的值")
                modify_store_remain_total(i[0],int(i[2]) + 1000)
                time.sleep(3)
                #print("修改状态为1")
                modify_status(i[0])
                time.sleep(time_sleep)

def main():
    get_data_to_csv()
    a = True
    while a:
        Y = input("请前往修改预设值，修改完成后，请输入大写的Y或者小写的y")
        if Y == "Y" or Y == "y":
            compare_data()
            a = False
            print("请输入任意键退出程序")
            input()
        else:
            print("输入有误，请重新输入")

config = toml.load("config.toml")
my_cookie = config["basic"]["mycookie"]
time_sleep = config["basic"]["timesleep"]
main()