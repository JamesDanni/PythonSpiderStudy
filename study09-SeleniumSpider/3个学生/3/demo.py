from selenium import webdriver

#大学总分排名信息列表
university_data_list = []
#大学生生源质量排名
university_data_list_life = []
#大学生培养结果（就业率）排名
university_data_list_work = []
#大学生社会声誉（社会捐赠收入）排名
university_data_list_money = []
#大学生科研规模排名
university_data_list_guimo = []
#大学生科研质量排名
university_data_list_zhiliang = []

# 获取列表的第四个元素
def takeSecond(elem):
    return elem[3]

def china_university():
    #需要获取的网页地址
    url = "http://www.zuihaodaxue.com/zuihaodaxuepaiming2019.html"
    driver = webdriver.Chrome()
    #浏览器最大化
    driver.maximize_window()
    #浏览器中输入需要访问的网页地址
    driver.get(url)
    #大学排名信息
    university_data = driver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/div/div[3]/div/table/tbody/tr')
    for i in university_data:
        print("爬取第%d所大学数据内容"%(len(university_data_list)+1))
        #总分排名NO
        num = i.find_element_by_xpath('./td[1]').text
        #学校名称
        name = i.find_element_by_xpath('./td[2]/div').text
        #学校所在城市
        city = i.find_element_by_xpath('./td[3]').text
        #总分
        all_grade = i.find_element_by_xpath('./td[4]').text
        #生源质量得分
        life_grade = i.find_element_by_xpath('./td[5]').text
        #就业率
        work_grade = i.find_element_by_xpath('./td[6]').text
        #社会声誉
        money = i.find_element_by_xpath('./td[7]').text
        #科研规模
        guimo = i.find_element_by_xpath('./td[8]').text
        #科研质量
        zhiliang = i.find_element_by_xpath('./td[9]').text
        university_data_list.append([num,name,city,all_grade])
        university_data_list_life.append([num,name,city,life_grade])
        university_data_list_work.append([num,name,city,work_grade])
        university_data_list_money.append([num,name,city,money])
        university_data_list_guimo.append([num,name,city,guimo])
        university_data_list_zhiliang.append([num,name,city,zhiliang])
    print("爬取数据结束")
    print("即将对数据结果排序")
    #对结果进行排序，按得分字段进行降序排列
    university_data_list_life.sort(key=takeSecond, reverse=True)
    university_data_list_work.sort(key=takeSecond, reverse=True)
    university_data_list_money.sort(key=takeSecond, reverse=True)
    university_data_list_guimo.sort(key=takeSecond, reverse=True)
    university_data_list_zhiliang.sort(key=takeSecond, reverse=True)
    print("数据排序结束")

#保存数据到文件中
def save_university_data(name,data_list):
    print("保存%s！"%name)
    try:
        f1 = open("%s.txt"%name,"w",encoding="utf-8")
        print("save data")
        for data in data_list:
            for i in data:
                f1.write(i.ljust(10, "　"))
            f1.write('\n')
        f1.close()
        print("%s保存成功！"%name)
    except:
        print("%s保存失败！"%name)

if __name__ == '__main__':
    china_university()
    name = ["总分排名","生源质量排名","结业率排名","社会声誉排名","科研规模排名","科研质量排名"]
    data_list = [university_data_list,
                 university_data_list_life,
                 university_data_list_work,
                 university_data_list_money,
                 university_data_list_guimo,
                 university_data_list_zhiliang]
    for i in range(len(name)):
        save_university_data(name[i],data_list[i])
        print("%s TOP10:"%name,data_list[:10])
        