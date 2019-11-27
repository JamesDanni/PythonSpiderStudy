#coding=utf-8

import requests
import json
from urllib import parse

url = ""
ret = requests.get(url)

params = {}
ret = requests.get(url,params = params)

data = {}  #form-data  dict直接传
ret = requests.post(url,data = data)

body = {}  #post body
body = json.JSONEncoder().encode(body)
ret = requests.post(url,body)

string_data = ""
params = parse.quote(string_data)  #对字符串进行url编码
params = {"test":"test"}
params = parse.urlencode(params)   #对params进行url编码

ret = requests.get(url,stream=True)  #stream为true时，等数据传输完再返回完整数据

ret = requests.get(url,allow_redirects=False)  #可以获取response header
print(ret.headers["location"])