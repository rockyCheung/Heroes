# -*- coding: utf-8 -*-
import email
from papa_office.models.MongoModels import Emails,UserEmailPreferences,User
from papa_office.mail.ReceiveEmail import ReceiveEmail

class EmailParser(object):

    def __init__(self):
        pass

    def parseEmailAndSave(self,mesgItems,userEmail):
        emailList = []
        for msgid, data in mesgItems.items():
            emailDict = {}
            paser = email.message_from_string(data[b'RFC822'])
            subject, efrom, content,chatset = self.parseEmailDetail(paser)
            emailDict['msgid'] = msgid
            emailDict['subject'] = subject
            emailDict['efrom'] = efrom
            emailDict['content'] = content
            emailDict['internaldate'] = data[b'INTERNALDATE']
            emailDict['flags'] = data[b'FLAGS']
            emailDict['chatset'] = chatset
            emailList.append(emailDict)
            Emails(userEmail,msgid,efrom,'',subject,data[b'INTERNALDATE'],content,chatset,data[b'FLAGS']).save()
        return emailList

    def parseEmailDetail(self,paser):
        subject = paser.get("subject")
        dh = email.Header.decode_header(subject)
        subject = str(dh[0][0]).decode(dh[0][1])
        efrom = email.utils.parseaddr(paser.get("from"))[1]
        # eto = email.utils.parseaddr(paser.get("to"))[1]
        content = ''
        for part in paser.walk():
            # fileName = part.get_filename()
            contentType = part.get_content_type()
            chatset = part.get_content_charset();
            if contentType == 'text/plain' or contentType == 'text/html':
                content = part.get_payload(decode=True)
                content = content.decode(chatset)
                break
        return subject,efrom,content,chatset
#多线程任务
    def mailWorker(self,userEmail):
        preferences = UserEmailPreferences.objects.get({'_id':userEmail,'enabled': True,'stype':0})
        for p in  preferences:
            # p.imap_server
            # p.imap_port
            # p.uname
            # p.upassword
            server = ReceiveEmail(host=p.imap_server, port=p.imap_port)
            server.login(p.uname, p.upassword)
            boxInfo = server.selectBox(boxName='INBOX')
            # print boxInfo['EXISTS']
            notDeleteList = server.searchNotDelete()
            # print notDeleteList
            mailInfo = server.fetchEmail(notDeleteList[0])
            parser = EmailParser()
            list = parser.parseEmailAndSave(mailInfo, userEmail)
            # print list
            server.logout()
#定时执行
    def dealAllUsersMail(self):
        users = User.objects.get({'status':0})
        for user in users:
            self.mailWorker(user.email)
