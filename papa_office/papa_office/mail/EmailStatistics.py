# -*- coding: utf-8 -*-
from django.core.management.base import AppCommand
from papa_office.mail.FeatureUpdateStatistics import  EmailStatisticsManager


class EmailStatistics(AppCommand):
    def handle(self, *args, **options):
        EmailStatisticsManager().update_statistics()