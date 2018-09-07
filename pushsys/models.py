# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class JPushSecret(models.Model):
    app_key = models.CharField(max_length=256)
    master_secret = models.CharField(max_length=256)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    production = models.BooleanField(default=True)

    class Meta:
        verbose_name = '推送消息'
        verbose_name_plural = verbose_name


class PushTemplate(models.Model):
    template_name = models.CharField(max_length=256, verbose_name='模板名称')
    template = models.TextField(verbose_name='模板内容')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    push_state_name = models.CharField(max_length=64, db_index=True, null=True, blank=True, verbose_name='推送状态')
    push_ctx = models.CharField(max_length=1024, null=True, blank=True, verbose_name='CTX')
    in_use = models.BooleanField(default=True, db_index=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '推送模板'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s: %s" % (self.template_name, self.push_state_name if self.push_state_name is not None else "None")
