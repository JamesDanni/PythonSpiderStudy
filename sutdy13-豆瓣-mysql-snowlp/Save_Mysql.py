#coding=utf-8

import pymysql

class SaveToMysql():
    def __init__(self,servaddr,username,password,db,table):
        self.servaddr = servaddr
        self.username = username
        self.password = password
        self.database = db
        self.table_name = table

    def conn_mysql(self):
        '''
        数据库连接
        :return:
        '''
        try:
            conn = pymysql.connect(self.servaddr,
                                   user = self.username,
                                   passwd = self.password,
                                   db = self.database)
            return conn
        except:
            print('连接数据库失败!')
            return None

    def create_table(self):
        '''
        创建表
        :return:
        '''
        conn = self.conn_mysql()
        cursor = conn.cursor()
        # 创建user表
        cursor.execute('drop table if exists %s'%self.table_name)
        sql = """CREATE TABLE IF NOT EXISTS %s (
        	  `id` int(11) NOT NULL AUTO_INCREMENT,
        	  `moviename` varchar(200),
        	  `movieappraise` varchar(500),
        	  `movieurl` varchar(100),
        	  PRIMARY KEY (`id`)
        	) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""%self.table_name
        cursor.execute(sql)
        conn.commit()
        cursor.close()  # 先关闭游标
        conn.close()  # 再关闭数据库连接

    def insert_data(self,data):
        '''
        插入数据
        :param data:
        :return:
        '''
        try:
            conn = self.conn_mysql()
            cursor = conn.cursor()
            sql = "INSERT INTO %s (moviename,movieappraise,movieurl)"%self.table_name
            sql = sql + " VALUES (%s,%s,%s)"
            cursor.executemany(sql,data)
            conn.commit()
            cursor.close()  # 先关闭游标
            conn.close()  # 再关闭数据库连接
        except:
            print("写入数据失败")

    def select_data(self):
        '''
        查询数据
        :return:
        '''
        conn = self.conn_mysql()
        cursor = conn.cursor()
        sql = "SELECT movieappraise from %s"%self.table_name
        cursor.execute(sql)
        ret = cursor.fetchall()
        return ret
