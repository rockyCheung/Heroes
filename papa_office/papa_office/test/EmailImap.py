# -*- coding: utf-8 -*-

import imaplib
import email  #导入两个库
import sys

def imapMailReceive():
    reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
    sys.setdefaultencoding('utf-8')
    try:
        conn = imaplib.IMAP4_SSL(port = '993',host = 'imap.exmail.qq.com')
        print('已连接服务器')
        conn.login('zhangpenghong@pengpengw.com','Roc7758521')

        print('已登陆')
        result, message = conn.select()
        print result, message
        type, data = conn.search(None, 'ALL')
        print type,data
        newlist=data[0].split()
        print newlist
        type1, data1 = conn.fetch(newlist[0], '(RFC822)')
        print type1,data1
        msg = email.message_from_string(data1[0])
        # .decode('utf-8')
        sub = msg.get('subject')
        print sub

        subdecode = email.header.decode_header(sub)[0][0]

        #打印标题
        print(subdecode.decode('utf-8'))

        for part in msg.walk():
         # 如果ture的话内容是没用的
            if not part.is_multipart():
                print(part.get_payload(decode=True).decode('utf-8'))
                # 解码出文本内容，直接输出来就可以了。
    except Exception, e:
        error_message=e.message
        print error_message

    finally:
        print conn.state
        conn.logout()
        if conn.state == 'SELECTED':
            conn.close()



imapMailReceive()