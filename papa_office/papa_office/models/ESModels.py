from django.db import models
from papa_office.es.models import EsIndexable
from django.conf import settings

# ELASTICSEARCH_URL = 'http://192.168.1.171:9100'
# settings.configure()
class M(EsIndexable, models.Model):
    # BGRQDateTime = models.DateTimeField()
    address = models.CharField()
    outputValue = models.CharField()
    # ExecutiveCourt = models.CharField()
    # mongo_id = models.CharField()
    # URL = models.CharField()
    # ExposureDate = models.DateField()
    # Name = models.CharField()
    # uid = models.CharField()
    # TheAmountOfTheSubject = models.IntegerField()
    # ImplementationBasis = models.CharField()
    # log_entry = models.CharField()
    IDcard = models.CharField()
    # logdate = models.DateTimeField()
    # UnappliedAmount = models.IntegerField()
    # CaseNumber = models.CharField()
    # DateOfFiling = models.DateField()
    # ImplementationCase = models.CharField()
    # foo = models.CharField(max_length=64)
# export DJANGO_SETTINGS_MODULE = ''
# settings.configure()

# print settings.__dict__
# q = M.es.all()#search('3308211963',facets=['IDcard'])
# print q