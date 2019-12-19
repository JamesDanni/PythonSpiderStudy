#coding=utf-8

import pymssql

def conn_baidu():
    # 连接数据库
    connect = pymssql.connect('127.0.0.1:1433', 'sa', '123456', 'test') #服务器名,账户,密码,数据库名
    if connect:
        pass
    else:
        print("连接数据库失败")
    return connect

def conn_poly():
    # 连接数据库
    connect = pymssql.connect('127.0.0.1:1433', 'sa', '123456', 'test') #服务器名,账户,密码,数据库名
    if connect:
        pass
    else:
        # 连接失败的话打印
        print("连接数据库失败")
    return connect

def create_baidutable_data():
    # 连接数据库
    conn = conn_baidu()
    # 创建数据游标
    cursor = conn.cursor()
    # 创建表格
    cursor.execute("""
    IF OBJECT_ID('BaiduSpiderTable', 'u') IS NOT NULL
        DROP TABLE BaiduSpiderTable
    CREATE TABLE BaiduSpiderTable (
        title VARCHAR(6000),
        time_release VARCHAR(100),
        content VARCHAR(6000),
        news_url VARCHAR(6000)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insertinto_baidutable(data):
    # 连接数据库
    conn = conn_baidu()
    # 创建游标
    cursor = conn.cursor()
    # 编写插入数据sql语句
    sql = "insert into BaiduSpiderTable(title,time_release,content,news_url) values(%s, %s, %s, %s)"
    for i in data:
        save_data = tuple(i)
        # 执行插入数据sql
        cursor.execute(sql,save_data)
    conn.commit()
    cursor.close()
    conn.close()

def create_polytable_data():
    # 连接数据库
    conn = conn_poly()
    # 创建游标
    cursor = conn.cursor()
    # 创建表
    cursor.execute("""
    IF OBJECT_ID('PolySpiderTable', 'u') IS NOT NULL
        DROP TABLE PolySpiderTable
    CREATE TABLE PolySpiderTable (
        title VARCHAR(6000),
        time_release VARCHAR(100),
        content VARCHAR(8000),
        news_url VARCHAR(6000)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insertinto_polytable(data):
    # 连接数据库
    conn = conn_poly()
    # 创建游标
    cursor = conn.cursor()
    # 编写数据库sql语句
    sql = "insert into PolySpiderTable(title,time_release,content,news_url) values(%s, %s, %s, %s)"
    save_data = tuple(data)
    # 执行sql语句
    cursor.execute(sql,save_data)
    conn.commit()
    cursor.close()
    conn.close()