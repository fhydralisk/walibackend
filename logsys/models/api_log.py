# coding=utf-8
from django.db import models
from usersys.models.usermodel import UserBase


class ApiLog(models.Model):
    visitor = models.ForeignKey(UserBase, verbose_name='访客', blank=True, null=True, )
    log_date_time = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=100)
