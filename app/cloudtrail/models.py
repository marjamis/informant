from datetime import datetime
from django.db import models

# Create your models here.


class Searches(models.Model):
    # django automatically adds a primary key of name id
    search_date = models.DateTimeField(default=datetime.now, blank=True)
    search_key = models.CharField(max_length=30)
    account = models.IntegerField(blank=True)
    location = models.CharField(max_length=50)
    data_date = models.DateTimeField()

    def __str__(self):        # __unicode__ on Python 2
        return self.search_key


class Files(models.Model):
    file = models.FileField()
