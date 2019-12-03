import requests
from bs4 import BeautifulSoup
from lxml import etree
import csv

# 抓取豆瓣小说的 书名、评分；

def html_data(page):
    # for u in range(0, 20):  # 循环20次，每一次循环爬取一页，即：抓取20页；
        basic_url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=' + str(page) + '&type=T'
        page += 20  # 每循环一次 +20，适应链接变化；
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        # 发送请求
        response = requests.get(basic_url, headers=headers, timeout=10)  # requests请求；
        response.encoding = 'utf-8'  # 设置编码
        htm = response.text  # 返回text文本；
        return htm

def jiexi(htm):
    lists_book = []  # 定义书名列表；
    lists_grade = []  # 定义评分的列表；
    book_info_list = []  # 定义书籍作者、出版社、出版日期、价格列表；
    book_data = []  # 定义抓取的书籍信息列表
    # 解析请求
    selector = etree.HTML(htm)  # 利用 etree.HTML 初始化
    book_name = selector.xpath('//*[@id="subject_list"]/ul/li/div[2]/h2/a/text()')  # 获取书名
    grade = selector.xpath('//*[@id="subject_list"]/ul/li/div[2]/div[2]/span[2]/text()')  # 获取评分；
    book_infos = selector.xpath('//*[@id="subject_list"]/ul/li/div[2]/div[1]/text()') #获取作者/出版社/时间/价格
    book_url = selector.xpath('//*[@id="subject_list"]/ul/li/div[1]/a/@href')
    # 将书名存入到lists_book列表；
    for i in book_name:
        lists_book.append(i.strip())  # 去除字符串空格，存入列表；
        while '' in lists_book:  # 如果列表中有空元素，则删除空元素；
            lists_book.remove('')
    # 将评分存入到lists_grade列表；
    for i in grade:
        lists_grade.append(i.strip())  # 去除字符串空格，存入列表；
        while '' in lists_grade:  # 如果列表中有空元素，则删除空元素；
            lists_grade.remove('')
    # 将书籍信息存如到book_info_list列表
    for i in book_infos:
        book_info = str(i).split('/')
        if len(book_info) == 5:
            book_info_list.append(book_info)
        if len(book_info) == 4:
            book_info_list.append([book_info[0],"",book_info[1],book_info[2],book_info[3]])
    for i in range(len(lists_book)):  #拼接书籍所有信息
        book_data.append([lists_book[i],  #书名
                          lists_grade[i], #评分
                          book_info_list[i][0].replace('\n', '').strip(), #作者，去掉换行符、空格符
                          book_info_list[i][1], #译者
                          book_info_list[i][2], #发版设
                          book_info_list[i][3], #发版日期
                          book_info_list[i][4], #价格
                          book_url[i]])  #书籍地址
    return book_data

def save(book_data):  #保存爬取结果
    csv_file = open("豆瓣小说数据.csv","w",encoding="utf-8",newline="")  #newline=""表示每行之间不写入一个空行
    c = csv.writer(csv_file)
    c.writerow(["书名","评分","作者","译者","出版社","出版日期","价格","书籍地址"])  #第一行写列名称
    for i in book_data:
        c.writerow(i)

def takeSecond(elem):
    return elem[1]

def top_30():
    top30_list = []  # 定义评分列表，存放书名、评分
    csv_file = open("豆瓣小说数据.csv", "r",encoding="utf-8")
    c = csv.reader(csv_file)
    for (k, v) in enumerate(c):  #读取爬取结果，并读取书名、书名评分
        if k == 0:
            continue
        top30_list.append([v[0],v[1]])  #将书名，书名评分存入评分列表中
    top30_list.sort(key = takeSecond,reverse=True)  #对评分列进行排序
    for i in top30_list[0:30]:
        print(i[0])

if __name__ == '__main__':
    count = 3  #定义爬取页数
    for page in range(count):
        htm = html_data(page)
        book_data = jiexi(htm)
        save(book_data)
    top_30()  #输出评分排名前30