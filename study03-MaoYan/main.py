#coding=utf-8
import requests
import re
import csv

def get_data(url):
    headers = {
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    try:
        ret = requests.get(url,headers = headers)
        ret.raise_for_status()
        return ret.text
    except:
        print("get_url_data fail!")
        return None

def paraise_data(data):
    pattren = re.compile('<dd>.*?board-index-.*?>(.*?)</i>.*?name.*?a.*?>(.*?)</a>.*?releasetime\">' +
                         '(.*?)</p>',re.S)
    data = re.findall(pattren,data)
    return data

def save_data(data):
    with open("test.csv","a",newline='') as f:
        f_csv = csv.writer(f)
        for i in data:
            f_csv.writerow(list(i))

url = "https://maoyan.com/board/4"
data = get_data(url)
data = paraise_data(data)
save_data(data)