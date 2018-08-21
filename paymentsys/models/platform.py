# coding=utf-8
from django.db import models


class PaymentPlatform(models.Model):
    description = models.TextField()
    module = models.CharField(max_length=256)
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '支付平台'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.description
