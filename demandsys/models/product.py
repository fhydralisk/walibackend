# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models


class ProductTypeL1(models.Model):
    tname1 = models.CharField(max_length=255, verbose_name=_("一级货物类型"))
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '货物一级分类'
        verbose_name_plural = '货物一级分类'

    def __unicode__(self):
        return self.tname1


class ProductTypeL2(models.Model):
    tname2 = models.CharField(max_length=255, verbose_name=_("2nd level product type"))
    t1id = models.ForeignKey(ProductTypeL1, related_name="product_l2")
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '货物二级分类'
        verbose_name_plural = '货物二级分类'

    def __unicode__(self):
        return self.tname2


class ProductTypeL3(models.Model):
    tname3 = models.CharField(max_length=255, verbose_name=_(u"三级货物类型"))
    t2id = models.ForeignKey(ProductTypeL2, related_name="product_l3")
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '货物三级分类'
        verbose_name_plural = '货物三级分类'

    def __unicode__(self):
        return self.tname3


class ProductQuality(models.Model):
    pqdesc = models.CharField(max_length=255, verbose_name=_("Quality description"))
    ord = models.IntegerField(verbose_name=_("Order field"))
    t3id = models.ForeignKey(ProductTypeL3, related_name="quality")
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '产品质量'
        verbose_name_plural = '产品质量'

    def __unicode__(self):
        return self.pqdesc


class ProductWaterContent(models.Model):
    pwcdesc = models.CharField(max_length=255, verbose_name=_("Water content description"))
    ord = models.IntegerField(verbose_name=_("Order field"))
    in_use = models.BooleanField(default=True)

    class Meta:
        verbose_name = '含水量'
        verbose_name_plural = '含水量'

    def __unicode__(self):
        return self.pwcdesc
