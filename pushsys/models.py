# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class JPushSecret(models.Model):
    app_key = models.CharField(max_length=256)
    master_secret = models.CharField(max_length=256)
    upload_date = models.DateTimeField(auto_now_add=True)
    production = models.BooleanField(default=True)

    class Meta:
        verbose_name = '推送消息'
        verbose_name_plural = verbose_name


class PushTemplate(models.Model):
    template_name = models.CharField(max_length=256)
    template = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    push_state_name = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    push_ctx = models.CharField(max_length=1024, null=True, blank=True)
    in_use = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = '推送模板'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s: %s" % (self.template_name, self.push_state_name if self.push_state_name is not None else "None")
