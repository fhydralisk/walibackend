from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

import datetime
from base.util.timestamp import now

from django.db import models
from django.conf import settings
from base.exceptions import WLException
from coresys.models import CoreAddressProvince, CoreAddressCity, CoreAddressArea, CorePaymentMethod
from usersys.models import UserBase, UserAddressBook
from .product import ProductTypeL3, ProductQuality, ProductWaterContent
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
    pmid = models.ForeignKey(CorePaymentMethod)
    st_time = models.DateTimeField(auto_now_add=True, verbose_name=_("start time"))
    duration = models.FloatField()
    abid = models.ForeignKey(UserAddressBook, on_delete=models.SET_NULL, verbose_name=_("user address book"), null=True, blank=True)
    aid = models.ForeignKey(CoreAddressArea, blank=True, null=True)
    street = models.CharField(max_length=511, blank=True, null=True)
    description = models.TextField()
    comment = models.TextField()
    match = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description

    def validate_satisfy_demand(self, opposite_role, quantity):
        """
        Raise WLError if not satisfied.
        :param opposite_role:
        :param quantity:
        :return:
        """

        if not self.in_use:
            raise WLException(404, "No such demand - not in use")

        # Validate expire date
        # TODO: Check whether "now" works
        if self.st_time + datetime.timedelta(days=self.duration) < now():
            raise WLException(404, "No such demand - expire")

        if opposite_role == self.uid.role:
            raise WLException(404, "No such demand - role does not match")

        if quantity < self.min_quantity:
            raise WLException(403, "Min Quantity not satisfied")

        # Validate whether quantity meets quantity - satisfied
        if quantity > self.quantity_left():
            raise WLException(403, "Exceed max quantity")

        return

    def quantity_left(self):
        # TODO: Implement this
        return self.quantity


class ProductDemandPhoto(models.Model):
    dmid = models.ForeignKey(ProductDemand, on_delete=models.CASCADE, related_name="demand_photo", db_index=True)
    demand_photo = models.ImageField(upload_to=settings.UPLOAD_DEMAND_PHOTO)
    demand_photo_snapshot = models.FilePathField(null=True, blank=True)
    inuse = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    photo_desc = models.CharField(max_length=255)

    def __unicode__(self):
        return self.photo_desc

