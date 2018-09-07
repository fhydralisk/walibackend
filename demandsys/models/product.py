# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models


class ProductTypeL1(models.Model):
    tname1 = models.CharField(max_length=255, verbose_name=_("货物一级分类"))
    in_use = models.BooleanField(default=True, verbose_name=_("是否有效"))

    class Meta:
        verbose_name = '货物一级分类'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.tname1


class ProductTypeL2(models.Model):
    tname2 = models.CharField(max_length=255, verbose_name=_("货物二级种类"))
    t1id = models.ForeignKey(ProductTypeL1, related_name="product_l2", verbose_name=_("货物一级种类"))
    in_use = models.BooleanField(default=True, verbose_name=_("是否有效"))

    class Meta:
        verbose_name = '货物二级分类'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.tname2


class ProductTypeL3(models.Model):
    tname3 = models.CharField(max_length=255, verbose_name=_("货物三级种类"))
    t2id = models.ForeignKey(ProductTypeL2, related_name="product_l3", verbose_name=_("货物二级种类"))
    in_use = models.BooleanField(default=True, verbose_name=_("是否有效"))

    class Meta:
        verbose_name = '货物三级分类'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.tname3


class ProductQuality(models.Model):
    pqdesc = models.CharField(max_length=255, verbose_name=_("质量描述"))
    ord = models.IntegerField(verbose_name=_("等级"))
    t3id = models.ForeignKey(ProductTypeL3, related_name="quality", verbose_name='货物种类')
    in_use = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '产品质量'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.pqdesc


class ProductWaterContent(models.Model):
    pwcdesc = models.CharField(max_length=255, verbose_name=_("含水量描述"))
    ord = models.IntegerField(verbose_name=_("等级"))
    in_use = models.BooleanField(default=True, verbose_name=_("是否有效"))

    class Meta:
        verbose_name = '含水量'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.pwcdesc
