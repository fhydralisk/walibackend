from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.conf import settings
from coresys.models import CoreAddressProvince, CoreAddressCity, CoreAddressArea
from usersys.models import UserBase, UserAddressBook
from .product import ProductTypeL3, ProductQuality, ProductWaterContent
from .payment import ProductPaymentMethod
from .demand_enum import t_demand_choice, unit_choice


class ProductDemand(models.Model):
    uid = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="user_demand")
    t_demand = models.IntegerField(verbose_name=_("demand type"), max_length=t_demand_choice.MAX_LENGTH, choices=t_demand_choice.choice, db_index=True)
    pid = models.ForeignKey(ProductTypeL3, on_delete=models.CASCADE, related_name="product_demand", db_index=True)
    qid = models.ForeignKey(ProductQuality, related_name="product_quality")
    wcid = models.ForeignKey(ProductWaterContent, related_name="product_watercontent")
    quantity = models.FloatField()
    min_quantity = models.FloatField()
    price = models.FloatField()
    unit = models.IntegerField(max_length=unit_choice.MAX_LENGTH, choices=unit_choice.choice)
    pmid = models.ForeignKey(ProductPaymentMethod)
    st_time = models.DateTimeField(auto_now_add=True, verbose_name=_("start time"))
    duration = models.FloatField()
    abid = models.ForeignKey(UserAddressBook, on_delete=models.SET_NULL, verbose_name=_("user address book"), null=True)
    aid = models.ForeignKey(CoreAddressArea)
    acid = models.ForeignKey(CoreAddressCity)
    acpid = models.ForeignKey(CoreAddressProvince)
    street = models.CharField(max_length=511, blank=True, null=True)
    description = models.TextField()
    comment = models.TextField()
    match = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description


class ProductDemandPhoto(models.Model):
    dmid = models.ForeignKey(ProductDemand, on_delete=models.CASCADE, related_name="demand_photo", db_index=True)
    path = models.ImageField(upload_to=settings.UPLOAD_DEMAND_PHOTO)
    path_snapshot = models.ImageField(upload_to=settings.UPLOAD_DEMAND_PHOTO_SNAPSHOT)
    inuse = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    photo_desc = models.CharField(max_length=255)

    def __unicode__(self):
        return self.photo_desc

