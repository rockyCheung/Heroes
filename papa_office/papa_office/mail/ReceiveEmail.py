# -*- coding: utf-8 -*-
from papa_office.imapclient import IMAPClient
import email

class ReceiveEmail(object):

    def __init__(self,host,port):
        self.host = host
        self.port = port

    #用户登陆
    def login(self,userName,password):
        self.server = IMAPClient(self.host, self.port)
        self.server.login(userName, password)

    #选择邮件
    def selectBox(self,boxName='INBOX'):
        return self.server.select_folder(boxName)

    #搜索未删除邮件,返回搜索结果True or False和邮件数量
    def searchNotDelete(self):
        messages = self.server.search([b'NOT', b'DELETED'])
        return messages

    #搜索未阅读邮件,返回搜索结果True or False和邮件数量
    def searchUnseen(self):
        messages = self.server.search([u'UNSEEN'])
        return messages

    # 搜索所有邮件,返回搜索结果True or False和邮件数量
    def searchAll(self):
        messages = self.server.search(criteria='ALL')
        return messages

    #messages为search返回结果list，返回items
    def fetchEmail(self,messages):
        response = self.server.fetch(messages, ['FLAGS','SEQ','INTERNALDATE','From','RFC822'])
        return response

    #用户签退
    def logout(self):
        self.server.logout()