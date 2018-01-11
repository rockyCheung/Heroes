# -*- coding:utf-8 -*-
from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from papa_office.security.Pycrypt import Pycrypt
from papa_office.security.UUIDTools import *
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.core.exceptions import ValidationError
# from django.db.utils import IntegrityError
import time
# Connect to MongoDB first. PyMODM supports all URI options supported by
# PyMongo. Make sure also to specify a database in the connection string:
connect('mongodb://192.168.1.178:27017/cobra')

# Now let's define some Models.
class User(MongoModel):
    # Use 'email' as the '_id' field in MongoDB.
    email = fields.EmailField(primary_key=True)
    #用户全名
    fname = fields.CharField()
    password = fields.CharField()
    #用户创建日期
    cdate = fields.DateTimeField()
    #用户状态0：有效 1：锁定 2：删除
    status = fields.IntegerField()
    #用户密码加密使用分散因子
    salt = fields.CharField()
    #是否记忆标识0：不记忆 1：记忆
    remember = fields.IntegerField()

class Keys(MongoModel):
    #密钥
    key = fields.CharField(required=True)
    #密钥创建时间
    cdate = fields.DateTimeField(required=True)
    #密钥状态0:无效 1：有效
    status = fields.IntegerField(required=True)
    #系统标识 0：用户密钥 1：平台密钥
    sflag = fields.IntegerField(required=True)

class Post(MongoModel):
    # This field references the User model above.
    # It's stored as a bson.objectid.ObjectId in MongoDB.
    author = fields.ReferenceField(User)
    title = fields.CharField(max_length=100)
    content = fields.CharField()
    tags = fields.ListField(fields.CharField(max_length=20))
    # These Comment objects will be stored inside each Post document in the
    # database.
    comments = fields.EmbeddedDocumentListField('Comment')

    class Meta:
        # Text index on content can be used for text search.
        indexes = [IndexModel([('content', TEXT)])]

# This is an "embedded" model and will be stored as a sub-document.
class Comment(EmbeddedMongoModel):
    author = fields.ReferenceField(User)
    body = fields.CharField()
    vote_score = fields.IntegerField(min_value=0)


class EmailLog(MongoModel):
    email = fields.EmailField(primary_key=True)
    subject = fields.CharField(max_length=100,blank=True)  # max_length=100 to store just the beginning of the subject
    date = fields.DateTimeField()
    success = fields.BooleanField(default=True)
    error = fields.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'%s: %s' % (self.email, self.subject)

    @staticmethod
    def create_log(email, subject, success=True, error=None):
        if error:
            if success:
                error = None  # to avoid inconsistent data caused by bad use of this method
            else:
                error = error[0:255]
        return EmailLog.objects.create(email=email, subject=subject[0:100], success=success, error=error)

class EmailStatistics(MongoModel):
    date = fields.DateTimeField()
    quantity = fields.IntegerField()

    def __unicode__(self):
        return u'%s' % self.date.strftime('%Y/%m/%d')

class EmailTypeManager(MongoModel):
    def all_types_that_users_can_disable(self):
        return self.filter(can_be_disabled=True).order_by('name')

class EmailType(MongoModel):
    name = fields.CharField(max_length=100)
    can_be_disabled = fields.BooleanField(default=True)

    objects = EmailTypeManager()

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.can_be_disabled:
            UserEmailPreferences.objects.filter(email_type=self).delete()
        super(EmailType, self).save(**kwargs)

class UserEmailPreferences(MongoModel):
    email = fields.EmailField(primary_key=True)
    #0:IMAP 1:POP 2:Exchange
    stype = fields.IntegerField(default=0)
    imap_server = fields.CharField(blank=True)
    imap_port = fields.IntegerField(blank=True)
    pop_server = fields.CharField(blank=True)
    pop_port = fields.IntegerField(blank=True)
    receive_ssl = fields.BooleanField(default=True)
    exchange_server = fields.CharField(blank=True)
    uname = fields.CharField(blank=True)
    upassword = fields.CharField(blank=True)
    # email_type = fields.ForeignKey(EmailType)
    enabled = fields.BooleanField(default=True)
    smtp_server = fields.CharField(blank=True)
    smtp_port = fields.IntegerField(blank=True)
    send_ssl = fields.BooleanField(default=True)
    # class Meta:
    #     unique_together = ('user', 'email_type')
    #
    # def save(self, **kwargs):
    #     if not self.enabled and not self.email_type.can_be_disabled:  # precaution to avoid inconsistent data
    #         raise ValidationError('This type of e-mail can not be disabled.')
    #     try:
    #         super(UserEmailPreferences, self).save(**kwargs)
    #     except IntegrityError:
    #         raise ValidationError('This type of e-mail has already been disabled.')

class EmailDatabase(MongoModel):
    email = fields.EmailField(primary_key=True)

def update_email_database(sender, instance, **kargs):
    if instance.email:
        EmailDatabase.objects.get_or_create(email=instance.email)

class Emails(MongoModel):
    userEmail = fields.EmailField()
    msgid = fields.IntegerField()
    efrom = fields.EmailField()
    eto = fields.EmailField(blank=True)
    subject = fields.CharField(max_length=100,blank=True)  # max_length=100 to store just the beginning of the subject
    internaldate = fields.DateTimeField()
    content = fields.CharField()
    charset = fields.CharField()
    flags = fields.CharField()



# Start the blog.
# We need to save these objects before referencing them later.
# today =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# keys = Keys('a!sxzd12$oknde#s',today,1,0).save()
# salt = UUIDTools.generateUUID()
# crpt = Pycrpt(key='a!sxzd12$oknde#s',salt=salt.get_hex())
# password = crpt.encrypt('123456')
# han_solo = User('admin@qq.com', 'Rocky.Cheung',password,today,0,salt,0).save()

# chewbacca = User(
#     'someoneelse@reallycoolmongostuff.com', 'Chewbacca', 'Thomas').save()


# post = BlogPost(
#     # Since this is a ReferenceField, we had to save han_solo first.
#     author=han_solo,
#     title="Five Crazy Health Foods Jabba Eats.",
#     content="...",
#     tags=['alien health', 'slideshow', 'jabba', 'huts'],
#     comments=[
#         Comment(author=han_solo, body='Rrrrrrrrrrrrrrrr!', vote_score=42)
#     ]
# ).save()

# keys = Keys.objects.get({'status': 1,'sflag':0})
# print keys.key
# for key in keys:
#     print(key.key + ' ')
# Find objects using familiar MongoDB-style syntax.
# slideshows = BlogPost.objects.raw({'tags': 'slideshow'})

# Only retrieve the 'title' field.
# slideshow_titles = slideshows.only('title')

# u'Five Crazy Health Foods Jabba Eats.'
# print(slideshow_titles.first().title)

