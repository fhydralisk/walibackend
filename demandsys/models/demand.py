from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

import datetime
from base.util.timestamp import now

from django.db import models
from django.conf import settings
from base.exceptions import WLException
from coresys.models import CoreAddressArea, CorePaymentMethod
from usersys.models import UserBase, UserAddressBook
from .product import ProductTypeL3, ProductQuality, ProductWaterContent
from demandsys.model_choices.demand_enum import t_demand_choice, unit_choice, freight_payer_choice
from demandsys.util.unit_converter import UnitQuantityMetric, UnitPriceMetric


def calc_score_by_operator(m1, m2, score_tuple):
    return score_tuple[1] if m1 == m2 else score_tuple[0] if m1 < m2 else score_tuple[2]


class ProductDemand(models.Model):
    uid = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="user_demand")
    t_demand = models.IntegerField(verbose_name=_("demand type"), choices=t_demand_choice.choice, db_index=True)
    pid = models.ForeignKey(ProductTypeL3, on_delete=models.CASCADE, related_name="product_demand", db_index=True)
    qid = models.ForeignKey(ProductQuality, related_name="product_quality")
    wcid = models.ForeignKey(ProductWaterContent, related_name="product_watercontent")
    quantity = models.FloatField()
    min_quantity = models.FloatField()
    price = models.FloatField()
    unit = models.IntegerField(choices=unit_choice.choice)
    pmid = models.ForeignKey(CorePaymentMethod)
    st_time = models.DateTimeField(auto_now_add=True, verbose_name=_("start time"))
    end_time = models.DateTimeField()
    abid = models.ForeignKey(
        UserAddressBook,
        on_delete=models.SET_NULL,
        verbose_name=_("user address book"),
        null=True,
        blank=True
    )
    aid = models.ForeignKey(CoreAddressArea, blank=True, null=True)
    street = models.CharField(max_length=511, blank=True, null=True)
    description = models.TextField()
    comment = models.TextField(blank=True, null=True)
    match = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    freight_payer = models.IntegerField(
        choices=freight_payer_choice.choice,
        default=freight_payer_choice.FREIGHT_SELLER
    )
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description

    def price_metric(self):
        return UnitPriceMetric(self.price, self.unit)

    def quantity_metric(self):
        return UnitQuantityMetric(self.quantity, self.unit)

    def validate_satisfy_demand(self, opposite_role, quantity=None, quantity_metric=None):
        """
        Raise WLError if not satisfied.
        :param opposite_role:
        :param quantity_metric:
        :param quantity:
        :return:
        """

        if quantity_metric is None:
            quantity_metric = UnitQuantityMetric(quantity, self.unit)

        if not self.in_use:
            raise WLException(404, "No such demand - not in use")

        # Validate expire date
        # TODO: Check whether "now" works
        if self.end_time < now():
            raise WLException(404, "No such demand - expire")

        if opposite_role == self.uid.role:
            raise WLException(404, "No such demand - role does not match")

        if quantity_metric < self.min_quantity_metric():
            raise WLException(403, "Min Quantity not satisfied")

        # Validate whether quantity meets quantity - satisfied
        if quantity_metric > self.quantity_left():
            raise WLException(403, "Exceed max quantity")

        return

    def quantity_left(self):
        # TODO: Implement this
        return UnitQuantityMetric(self.quantity, self.unit)

    def min_quantity_metric(self):
        return UnitQuantityMetric(self.min_quantity, self.unit)

    @property
    def is_expired(self):
        return self.end_time < now()

    @property
    def duration(self):
        return (self.end_time - self.st_time).days

    @property
    def expired_after_days(self):
        return max((self.end_time - now() + datetime.timedelta(days=0.5)).days, 0)

    @duration.setter
    def duration(self, value):
        self.end_time = now() + datetime.timedelta(days=value)

    def match_score(self, other):
        # type: (self.__class__) -> dict
        score_water = calc_score_by_operator(self.wcid.ord, other.wcid.ord, (1, 0, -1))
        score_price = calc_score_by_operator(self.price_metric(), other.price_metric(), (1, 0, -1))
        score_paymethod = calc_score_by_operator(self.pmid.ord, other.pmid.ord, (1, 0, -1))
        score_area = 1 if self.aid == other.aid else 0 if self.aid.cid == other.aid.cid else -1
        score_total = score_water + score_price + score_paymethod + score_area

        return {
            "score_water": score_water,
            "score_area": score_area,
            "score_paymethod": score_paymethod,
            "score_price": score_price,
            "score_overall": score_total
        }


class ProductDemandPhoto(models.Model):
    dmid = models.ForeignKey(ProductDemand, on_delete=models.SET_NULL, related_name="demand_photo", db_index=True, null=True, blank=True)
    demand_photo = models.ImageField(upload_to=settings.UPLOAD_DEMAND_PHOTO)
    demand_photo_snapshot = models.FilePathField(null=True, blank=True)
    inuse = models.BooleanField(default=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    photo_desc = models.CharField(max_length=255)

    def __unicode__(self):
        return self.photo_desc
