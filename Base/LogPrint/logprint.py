import logging

logging.basicConfig(                                                       #通过具体的参数来更改logging模块默认行为；
    level=logging.ERROR,                                                   #设置告警级别为ERROR；
    format="%(asctime)s--%(pathname)s--%(lineno)d-- %(message)s",          #自定义打印的格式；
    filename="log.txt",                                                    #将日志输出到指定的文件中；
    filemode="w",                                                          # w:覆盖方式  a:追加方式;
)

"""
format参数中可能用到的格式化串:
    1>.%(name)s
         Logger的名字
    2>.%(levelno)s
        数字形式的日志级别
    3>.%(levelname)s
        文本形式的日志级别
    4>.%(pathname)s
        调用日志输出函数的模块的完整路径名，可能没有
    5>.%(filename)s
        调用日志输出函数的模块的文件名
    6>.%(module)s
        调用日志输出函数的模块名
    7>.%(funcName)s
        调用日志输出函数的函数名
    8>.%(lineno)d
        调用日志输出函数的语句所在的代码行
    9>.%(created)f
        当前时间，用UNIX标准的表示时间的浮 点数表示
    10>.%(relativeCreated)d
        输出日志信息时的，自Logger创建以 来的毫秒数
    11>.%(asctime)s
        字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
    12>.%(thread)d
        线程ID。可能没有
    13>.%(threadName)s
        线程名。可能没有
    14>.%(process)d
        进程ID。可能没有
    15>.%(message)s
        用户输出的消息
"""


# logging.debug("debug message")              #告警级别最低，只有在诊断问题时才有兴趣的详细信息。
#
# logging.info("info message")                #告警级别比debug要高，确认事情按预期进行。
#
# logging.warning("warning message")          #告警级别比info要高，该模式是默认的告警级别！预示着一些意想不到的事情发生，或在不久的将来出现一些问题（例如“磁盘空间低”）。该软件仍在正常工作。
#
# logging.error("error message")              #告警级别要比warning药膏，由于一个更严重的问题，该软件还不能执行某些功能。
#
# logging.critical("critical message")        #告警级别要比error还要高，严重错误，表明程序本身可能无法继续运行。
