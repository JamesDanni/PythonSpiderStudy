#coding=utf-8
from threading import Thread

def eg_threading(a,b,c):
    for i in range(10):
        print(a)
        print(b)
        print(c)

def eg_threading_two():
    for i in range(10):
        print(11)
        # time.sleep(1)

a = Thread(target=eg_threading,args=(1,2,3))
b = Thread(target=eg_threading_two,args=(11,12))
a.start()  #启动线程
b.start()  #启动线程
a.join()   #等待线程执行完毕
b.join()   #等待线程执行完毕




def get_data():
    pass
def parase_data():
    pass
def save_data(lst):
    pass
#请求网页10次  处理数据10次
def main():
    data = get_data()
    lst = parase_data()
    save_data(lst)

treadlst = []
count = 10
for i in range(count):
    t = Thread(target=main,args=())
    treadlst.append(t)

for i in range(count):
    treadlst[i].start()

for i in range(count):
    treadlst[i].join()
