# coding=utf-8
from __future__ import unicode_literals

from .usermodel import UserBase

from django.db import models


class UserSid(models.Model):
    sid = models.CharField(max_length=128, primary_key=True)
    uid = models.ForeignKey(UserBase)
    last_ipaddr = models.GenericIPAddressField()
    generate_datetime = models.DateTimeField(auto_now_add=True)
    expire_datetime = models.DateTimeField()
    last_login = models.DateTimeField()
    is_login = models.BooleanField(default=False)

    class Meta:
        verbose_name = '用户sid'
        verbose_name_plural = '用户sid'

    def __unicode__(self):
        return "%s : %s" % (self.uid, self.sid)
