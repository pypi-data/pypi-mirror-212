# requirement

## 使用说明

```python
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
```

