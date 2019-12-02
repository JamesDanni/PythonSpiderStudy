#coding=utf-8

'''
PDF解析库的安装
pip install pdfplumber
'''

##获取pdf文件
# import requests
#
# url = "https://www.sf-express.com/cn/sc/download/20191016-IR-01-2019.PDF"
# ret = requests.get(url)
# f = open("1.pdf","wb")
# f.write(ret.content)
# f.close()

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator

password = ''
# 打开pdf文件
fp = open('1.pdf', 'rb')
# 从文件句柄创建一个pdf解析对象
parser = PDFParser(fp)
# 创建pdf文档对象，存储文档结构
document = PDFDocument(parser, password)
# 创建一个pdf资源管理对象，存储共享资源
rsrcmgr = PDFResourceManager()
laparams = LAParams()
# 创建一个device对象
# device = PDFDevice(rsrcmgr)
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
# 创建一个解释对象
interpreter = PDFPageInterpreter(rsrcmgr, device)
# 处理包含在文档中的每一页
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    layout = device.get_result()
    for x in layout:
        if isinstance(x, LTImage):  # 图片对象
            pass
        if isinstance(x, LTCurve):  # 曲线对象
            pass
        if isinstance(x, LTFigure):  # figure对象
            pass
        if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容
            # num_TextBoxHorizontal += 1  # 水平文本框对象增一
            # 保存文本内容
            with open(r'test.txt', 'a',encoding="utf-8-sig") as f:
                results = x.get_text()
                f.write(results + '\n')