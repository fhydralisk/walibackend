# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# FIXME, Chinese support?
class CoreAddressProvince(models.Model):
    province = models.CharField(max_length=50, verbose_name='省')
    in_use = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '省'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.province


class CoreAddressCity(models.Model):
    pid = models.ForeignKey(CoreAddressProvince, on_delete=models.CASCADE, related_name="city", verbose_name='省')
    city = models.CharField(max_length=50, verbose_name='市')
    in_use = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.city


class CoreAddressArea(models.Model):
    cid = models.ForeignKey(CoreAddressCity, on_delete=models.CASCADE, related_name="area", verbose_name='市')
    area = models.CharField(max_length=50, verbose_name='区')
    in_use = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '区'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.area
