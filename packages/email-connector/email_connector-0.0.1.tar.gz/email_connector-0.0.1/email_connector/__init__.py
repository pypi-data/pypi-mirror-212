import yamail
from imbox import Imbox


class SendEmail:
    def __init__(self, title, content, files=None):
        password = ""
        host = "smtp.qq.com"
        user = ""
        to = []
        cc = None

        smtp = yamail.SMTP(host=host, user=user, password=password)
        smtp.send(to=to, cc=cc, subject=title, contents=content, attachments=files)


class ReceiveEmail:
    """
        使用说明:
            1.实例化对象: ReceiveEmail(user, password, host)
                >>参数说明:
                    1.user: 邮箱账号
                    2.password: 邮箱密码
                    3.host: 邮箱服务器地址  --> 例如: smtp.qq.com
            2.get_attachment(): 获取邮件附件
                >>参数说明:
                    1.is_mark: 是否标记已读 True/False  --> 用于邮件操作, 标记已读后，下次获取邮件时，不会再获取到该邮件
                    2.is_delete: 是否删除邮件 True/False --> 用于邮件操作, 删除邮件后，下次获取邮件时，不会再获取到该邮件
                    3.**kwargs: 邮件过滤参数
                        :param subject: 邮件主题 str类型(必选)
                        :param unread: 是否未读邮件 True/False
                        :param flagged: 红旗标记邮件 True/False
                        :param date__lt: 某天前的邮件 date类型
                        :param date__gt: 某天后的邮件 date类型
                        :param date__on: 某天的邮件 date类型
                        :param sent_from: 指定发件人的邮件 str类型
                >>返回值:
                    1.返回一个列表, 列表中的元素为字典, 字典中包含邮件附件的文件名和文件内容
                        [
                            {
                                'uid': '29',
                                'date': 'Sat, 22 Apr 2023 08:53:51 -0000',
                                'subject': '测试',
                                'attachments': [
                                    {
                                        'content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                        'size': 9086,
                                        'content': <_io.BytesIO object at 0x0000016EFA10C770>,
                                        'content-id': None, 'filename': '=?utf-8?b?5qGj5L2N57q/5aKe5YqgLnhsc3g=?='
                                    },
                                ]
                            },
                        ]
                >>调用示例:
                    receive_email = ReceiveEmail(user='421085627@qq.com', password="jymniihawtwacaad")
                    info = receive_email.get_attachment(subject='测试', sent_from= '3003176737@qq.com', unread= False)
                    print(info)
            3.get_text(): 获取邮件正文
                >>使用场景:
                    1.获取邮件正文
                >>参数说明:
                    1.is_mark: 是否标记已读 True/False  --> 用于邮件操作, 标记已读后，下次获取邮件时，不会再获取到该邮件
                    2.is_delete: 是否删除邮件 True/False --> 用于邮件操作, 删除邮件后，下次获取邮件时，不会再获取到该邮件
                    3.**kwargs: 邮件过滤参数
                        :param subject: 邮件主题 str类型
                        :param unread: 是否未读邮件 True/False
                        :param flagged: 红旗标记邮件 True/False
                        :param date__lt: 某天前的邮件 date类型
                        :param date__gt: 某天后的邮件 date类型
                        :param date__on: 某天的邮件 date类型
                        :param sent_from: 指定发件人的邮件 str类型
                >>返回值:
                    1.返回一个列表, 列表中的元素为字典, 字典中包含邮件正文
                        [{'uid': '29', 'date': 'Sat, 22 Apr 2023 08:53:51 -0000', 'subject': '测试', 'content': ['测试发送邮件']}]

                >>调用示例:
                    receive_email = ReceiveEmail(user='421085627@qq.com', password="jymniihawtwacaad")
                    info = receive_email.get_text(sent_from= '3003176737@qq.com', unread= False)
                    print(info)
    """

    def __init__(self, user='', password="", host = "smtp.qq.com"):
        self.user = user
        self.password = password
        self.host = host

    def get_attachment(self, is_mark=False, is_delete=False, **kwargs):
        if not kwargs.get('subject', False):
            raise ValueError('subject must be in filters: 截取附件不指定主题, 你读个der啊')

        info = []
        messages = self.get_messages(**kwargs)
        for uid, message in messages:
            if message.subject == kwargs['subject']:
                info.append({
                    'uid': uid.decode(),                  # 邮件uid
                    'date': message.date,                 # 邮件发送时间
                    'subject': message.subject,           # 邮件主题
                    'attachments': message.attachments,   # 附件列表
                })
                self.last_operate(uid, is_mark, is_delete)

        self.imbox.logout()
        return info

    def get_text(self, is_mark=False, is_delete=False, **kwargs):
        def _func():
            info.append({
                'uid': uid.decode(),              # 邮件uid
                'date': message.date,             # 邮件发送时间
                'subject': message.subject,       # 邮件主题
                'content': message.body['plain'], # 邮件文本格式正文

            })
            self.last_operate(uid, is_mark, is_delete)

        info = []
        messages = self.get_messages(**kwargs)
        for uid, message in messages:
            # 如果有指定主题, 则筛选主题
            if kwargs.get('subject', False):
                if message.subject == kwargs['subject']:
                    _func()
            _func()

        self.imbox.logout()
        return info

    def get_messages(self, **kwargs):
        if kwargs.get('subject', False):
            del kwargs['subject']

        self.imbox = Imbox(self.host, self.user, self.password)
        return self.imbox.messages(**kwargs)  # 解包模式筛选邮件

    def last_operate(self, uid, is_mark, is_delete):
        """邮件操作: """
        if is_mark:
            self.imbox.mark_seen(uid) # 标记为已读
        if is_delete:
            self.imbox.delete(uid)  # 删除邮件



if __name__ == '__main__':
    # 数据筛选
    import time
    SendEmail('最后一次测试', '测试发送邮件', files=[r'C:\Users\majianli\Desktop\test.xlsx', r'C:\Users\majianli\Desktop\例子.xlsx'])
    time.sleep(10)
    receive_email = ReceiveEmail(user='421085627@qq.com', password="jymniihawtwacaad", host = "smtp.qq.com")
    info1 = receive_email.get_attachment(subject='最后一次测试', sent_from= '3003176737@qq.com', unread= True)
    info2 = receive_email.get_text(is_mark=True, sent_from= '3003176737@qq.com', unread= False)
    print(info1)
    print('='*100)
    print(info2)
