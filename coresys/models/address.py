# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# FIXME, Chinese support?
class CoreAddressProvince(models.Model):
    province = models.CharField(max_length=50)
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '省'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.province


class CoreAddressCity(models.Model):
    pid = models.ForeignKey(CoreAddressProvince, on_delete=models.CASCADE, related_name="city")
    city = models.CharField(max_length=50)
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.city


class CoreAddressArea(models.Model):
    cid = models.ForeignKey(CoreAddressCity, on_delete=models.CASCADE, related_name="area")
    area = models.CharField(max_length=50)
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '区'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.area
