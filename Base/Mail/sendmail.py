#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

class Send_Mail():
    '''
    邮件发送，可以附带任何形式的附件，邮件中附件名称为传入send函数的附件路径
    '''
    def __init__(self,smtp_host,smtp_port,send_user,send_password,recv_user):
        '''
        :param smtp_host:发送方的smtp服务器域名     string类型
        :param smtp_port: 发送方的smtp服务器端口号  int类型
        :param send_user: 发送方的邮箱地址          string类型
        :param send_password: 发送方的邮箱密码      string类型
        :param recv_user: 接收方的邮箱地址          string类型
        '''
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.send_user = send_user
        self.send_password = send_password
        self.recv_user = recv_user

    def send(self, mail_title,conten,file_path = ""):
        '''
        :param mail_title:邮件标题                         string类型
        :param conten: 邮件正文内容                        string类型
        :param file_path: 附件路径 默认为空，为空时不含附件  string类型
        :return:"success"/"fail"                          string类型
        '''
        message = MIMEMultipart()
        message['From'] = self.send_user
        message['To'] = self.recv_user
        message['Subject'] = Header(mail_title, 'utf-8')
        message.attach(MIMEText(conten, 'plain', 'utf-8'))
        if len(file_path) > 0:
            part_attach1 = MIMEApplication(open(file_path, 'rb').read())  # 打开附件
            part_attach1.add_header('Content-Disposition', 'attachment', filename=file_path)  # 为附件命名
            message.attach(part_attach1)  # 添加附件
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.smtp_host, self.smtp_port)
            smtpObj.login(self.send_user, self.send_password)
            smtpObj.sendmail(self.send_user, self.recv_user, message.as_string())
            return "success"
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件" + e.strerror)
            return "fail"

# s = Send_Mail("smtp.163.com",25,"发送方邮箱地址","发送方邮箱密码","接收的邮箱地址")
# s.send("邮件标题","邮件正文","附件路径")