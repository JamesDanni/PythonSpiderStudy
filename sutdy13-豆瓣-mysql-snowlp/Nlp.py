from snownlp import SnowNLP
import matplotlib.pyplot as pl


class DataVisual():
    def visual(self,movie,data):
        sentences = []
        senti_score = []
        for i in data:  #读取每一条评价内容
            movie_appraise = i[0]
            a1 = SnowNLP(movie_appraise)
            a2 = a1.sentiments
            sentences.append(i)  # 语序...
            senti_score.append(a2)  # 计算分值情况
        x = []
        for i in range(len(senti_score)):
            x.append(i+1)
        pl.rcParams['font.sans-serif']=['SimHei']  #设置图片显示中文字符
        pl.plot(x, senti_score)  #根据x轴,y轴画图
        pl.title(u'%s电影评价情感分析'%movie)  #图片结果标题
        pl.xlabel(u'评 论 用 户')  #图片中X轴名称
        pl.ylabel(u'情 感 程 度')  #图片中Y轴名称
        pl.savefig("%s感情分析结果.png"%movie)  #保存分析结果