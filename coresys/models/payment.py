# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models


class CorePaymentMethod(models.Model):
    ord = models.IntegerField(_("Order Number"))
    opmdesc = models.TextField(verbose_name=_("Description"), max_length=125)
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '支付方式'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.opmdesc
