# coding=utf-8
from __future__ import unicode_literals

from .usermodel import UserBase

from django.db import models


class UserSid(models.Model):
    sid = models.CharField(max_length=128, primary_key=True)
    uid = models.ForeignKey(UserBase, verbose_name='对应用户')
    last_ipaddr = models.GenericIPAddressField(verbose_name='上次登陆IP')
    generate_datetime = models.DateTimeField(auto_now_add=True, verbose_name='生成时间')
    expire_datetime = models.DateTimeField(verbose_name='失效时间')
    last_login = models.DateTimeField(verbose_name='上次登陆时间')
    is_login = models.BooleanField(default=False, verbose_name='登陆状态')

    class Meta:
        verbose_name = 'sid'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s : %s" % (self.uid, self.sid)
