from snownlp import SnowNLP
import pandas as pd
import matplotlib.pyplot as pl

txt = open('欧美喜剧.txt',"r",encoding="utf-8")
text = txt.readlines()
txt.close()
print('数据集读入成功')
sentences = []
senti_score = []
for i in text:  #读取每一条评价内容
    a1 = SnowNLP(i)
    a2 = a1.sentiments
    sentences.append(i)  # 语序...
    senti_score.append(a2)  # 计算分值情况
table = pd.DataFrame(sentences, senti_score)
x = []
for i in range(len(senti_score)):
    x.append(i+1)
pl.rcParams['font.sans-serif']=['SimHei']  #设置图片显示中文字符
pl.plot(x, senti_score)  #根据x轴,y轴画图
pl.title(u'电影评价情感分析')  #图片结果标题
pl.xlabel(u'评 论 用 户')  #图片中X轴名称
pl.ylabel(u'情 感 程 度')  #图片中Y轴名称
pl.savefig("欧美喜剧.png")  #保存分析结果
