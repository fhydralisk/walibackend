from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from walibackend.settings import UPLOAD_DEMAND_PHOTO


class ProductTypeL1(models.Model):
    tname1 = models.CharField(max_length=255, verbose_name=_("Top level product type"))
    in_use = models.BooleanField(default=True)
    default_photo = models.ImageField(upload_to=UPLOAD_DEMAND_PHOTO)

    def __unicode__(self):
        return self.tname1


class ProductTypeL2(models.Model):
    tname2 = models.CharField(max_length=255, verbose_name=_("2nd level product type"))
    t1id = models.ForeignKey(ProductTypeL1, related_name="product_l2")
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.tname2


class ProductTypeL3(models.Model):
    tname3 = models.CharField(max_length=255, verbose_name=_("3nd level product type"))
    t2id = models.ForeignKey(ProductTypeL2, related_name="product_l3")
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.tname3


class ProductQuality(models.Model):
    pqdesc = models.CharField(max_length=255, verbose_name=_("Quality description"))
    ord = models.IntegerField(verbose_name=_("Order field"))
    t3id = models.ForeignKey(ProductTypeL3, related_name="quality")
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.pqdesc


class ProductWaterContent(models.Model):
    pwcdesc = models.CharField(max_length=255, verbose_name=_("Water content description"))
    water_content = models.FloatField()
    ord = models.IntegerField(verbose_name=_("Order field"))
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.pwcdesc

