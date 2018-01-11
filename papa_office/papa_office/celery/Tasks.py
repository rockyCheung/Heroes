# -*- coding: utf-8 -*-
# from celery.decorators import task
from django.conf import settings
from celery import task
from papa_office.mail.FeatureSendEmail import EmailSender
from papa_office.mail.FeatureUpdateStatistics import EmailStatisticsManager
from papa_office.mail.EmailParser import EmailParser

# app = Celery('tasks', broker=BROKER_URL)
# app = Celery('tasks', broker='mongodb://192.168.1.178:27017/cobra')

@task(queue=settings.EMAIL_MANAGER_TASK if hasattr(settings, 'EMAIL_MANAGER_TASK') else None)
def send_email(emails, subject, text_content=None, html_content=None, main_content=None):
    EmailSender().send_email(emails, subject, text_content, html_content, main_content)


@task(queue=settings.EMAIL_MANAGER_TASK if hasattr(settings, 'EMAIL_MANAGER_TASK') else None)
def send_email_to_groups(groups, additional_emails, subject, content, html_content):
    EmailSender().send_email_to_groups(groups, additional_emails, subject, content, html_content)
    
    
@task(queue=settings.EMAIL_MANAGER_TASK if hasattr(settings, 'EMAIL_MANAGER_TASK') else None)
def send_email_to_users(users, additional_emails, subject, content, html_content):
    EmailSender().send_email_to_users(users, additional_emails, subject, content, html_content)
    

@task(queue=settings.EMAIL_MANAGER_TASK if hasattr(settings, 'EMAIL_MANAGER_TASK') else None)
def update_statistics():
    EmailStatisticsManager().update_statistics()

@task(queue=settings.EMAIL_MANAGER_TASK if hasattr(settings, 'EMAIL_MANAGER_TASK') else None)
def mail_receive(userEmail):
    emailParser = EmailParser()
    emailParser.mailWorker(userEmail)

@task(queue=settings.EMAIL_MANAGER_TASK if hasattr(settings, 'EMAIL_MANAGER_TASK') else None)
def mail_batch_receive():
    emailParser = EmailParser()
    emailParser.dealAllUsersMail()

@task
def add(x, y):
    return x + y
