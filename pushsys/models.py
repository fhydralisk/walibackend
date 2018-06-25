from __future__ import unicode_literals

from django.db import models

# Create your models here.


class JPushSecret(models.Model):
    app_key = models.CharField(max_length=256)
    master_secret = models.CharField(max_length=256)
    upload_date = models.DateTimeField(auto_now_add=True)


class PushTemplate(models.Model):
    template_id = models.IntegerField(unique=True, primary_key=True)
    template_name = models.CharField(max_length=256)
    template = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
