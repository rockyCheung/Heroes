# Copyright (c) 2014, Menno Smits
# Released subject to the New BSD License
# Please see http://en.wikipedia.org/wiki/BSD_licenses

from papa_office.imapclient import IMAPClient
import email
from papa_office.mail.ReceiveEmail import ReceiveEmail
from papa_office.mail.EmailParser import EmailParser

HOST = 'imap.exmail.qq.com'
USERNAME = 'zhangpenghong@pengpengw.com'
PASSWORD = 'Roc7758521'
serverNew = ReceiveEmail(host=HOST,port=993)
# server = IMAPClient(HOST,port=993)
# server.login(USERNAME, PASSWORD)
serverNew.login(USERNAME, PASSWORD)
boxInfo = serverNew.selectBox(boxName='INBOX')
print boxInfo['EXISTS']
notDeleteList = serverNew.searchNotDelete()
print notDeleteList
mailInfo = serverNew.fetchEmail(notDeleteList[0])
p = EmailParser()
list = p.parseEmailAndSave(mailInfo,'zhangpenghong@pengpengw.com')
print list
serverNew.logout()
# print mailInfo[0]['INTERNALDATE'],mailInfo['FLAGS'],mailInfo['From']
# select_info = server.select_folder('INBOX')
# print('%d messages in INBOX' % select_info[b'EXISTS'])
#
# messages = server.search(['NOT', 'DELETED'])
# print("%d messages that aren't deleted\n" % len(messages))
#
# print("Messages:",messages)
# response = server.fetch(messages[0], ['FLAGS', 'RFC822.SIZE'])
# response = server.fetch(messages[0], ['FLAGS','INTERNALDATE','RFC822'])
# print response
# for msgid, data in response.items():
#     # print('   ID %d: %d bytes, flags=%s' % (msgid,
#     #                                         data[b'RFC822.SIZE'],
#     #                                         data[b'FLAGS']))
#     # print data
#     j = 0
#     print '#########'
#     msg = email.message_from_string(data[b'RFC822'])
#     subject = msg.get("subject")
#     dh = email.Header.decode_header(subject)
#     subject = str(dh[0][0]).decode(dh[0][1])
#     froms = email.utils.parseaddr(msg.get("from"))
#     to = email.utils.parseaddr(msg.get("to"))
#     for part in msg.walk():
#         j = j + 1
#         fileName = part.get_filename()
#         contentType = part.get_content_type()
#         mycode = part.get_content_charset();
#
#         if contentType == 'text/plain' or contentType == 'text/html':
#             data = part.get_payload(decode=True)
#             content=str(data);
#             if mycode=='gb2312':
#                 content= str(content).decode('gb2312')
#
#                 print("nPos is %s",content)
#         else:
#             print contentType, mycode
#
#     #     print 'msg',msg.get("Content-Type")
#     # print '@',str(dh[0][0]).decode(dh[0][1])
#     # print '@@@',froms
#     # print('   ID %d: %s bytes, INTERNALDATE=%s ,Subject: %s' % (msgid,
#     #                                                str(data[b'RFC822']).decode(encoding='gb2312'),
#     #                                         data[b'INTERNALDATE'],'subject'))
#
# server.logout()
