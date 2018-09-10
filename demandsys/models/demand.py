from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

import datetime
from base.util.timestamp import now

from django.db import models
from django.conf import settings
from base.exceptions import WLException
from coresys.models import CoreAddressArea, CorePaymentMethod
from usersys.models import UserBase, UserAddressBook
from usersys.model_choices.user_enum import role_choice
from .product import ProductTypeL3, ProductQuality, ProductWaterContent
from demandsys.model_choices.demand_enum import t_demand_choice, freight_payer_choice, interval_choice


def calc_score_by_operator(m1, m2, score_tuple):
    return score_tuple[1] if m1 == m2 else score_tuple[0] if m1 < m2 else score_tuple[2]


class ProductDemand(models.Model):
    uid = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="user_demand")
    t_demand = models.IntegerField(verbose_name=_("demand type"), choices=t_demand_choice.choice, db_index=True)
    pid = models.ForeignKey(ProductTypeL3, on_delete=models.CASCADE, related_name="product_demand", db_index=True)
    qid = models.ForeignKey(ProductQuality, related_name="product_quality")
    wcid = models.ForeignKey(ProductWaterContent, related_name="product_watercontent")
    quantity = models.FloatField()
    min_quantity = models.FloatField(default=0)
    price = models.FloatField()
    pmid = models.ForeignKey(CorePaymentMethod, default=None, null=True)
    st_time = models.DateTimeField(auto_now=True, verbose_name=_("start time"))
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
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True, null=True)
    match = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    freight_payer = models.IntegerField(
        choices=freight_payer_choice.choice,
        default=None,
        null=True
    )
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description

    def validate_satisfy_demand(self, opposite_role, quantity=None):
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
        if self.end_time < now():
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
        from appraisalsys.models.appraise import AppraisalInfo
        counter_appraisal_quantity = AppraisalInfo.objects.filter(
            models.Q(ivid__dmid_s=self) | models.Q(ivid__dmid_t=self)
        ).aggregate(models.Sum('ivid__quantity'))['ivid__quantity__sum']
        if counter_appraisal_quantity is not None:
            return self.quantity - counter_appraisal_quantity if counter_appraisal_quantity < self.quantity else 0
        else:
            return self.quantity

    @property
    def is_expired(self):
        return self.end_time < now()

    # FIXME: maybe the create_time is better than st_time
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
        if self.uid.role == role_choice.SELLER:
            score_tuple = (1, 0, -1)
        elif self.uid.role == role_choice.BUYER:
            score_tuple = (-1, 0, 1)
        else:
            raise AssertionError("role of user should be seller or buyer but %d instead." % self.uid.role)

        score_water = calc_score_by_operator(self.wcid.ord, other.wcid.ord, score_tuple)
        score_price = calc_score_by_operator(self.price, other.price, score_tuple)

        score_area = 1 if self.aid == other.aid else 0 if self.aid.cid == other.aid.cid else -1
        score_total = score_water + score_price + score_area

        return {
            "score_water": score_water,
            "score_area": score_area,
            "score_price": score_price,
            "score_overall": score_total,
        }

    @property
    def last_modify_from_now(self):
        interval = now() - self.st_time
        if interval.total_seconds() < 3600:
            return interval_choice.JUST_NOW
        elif interval.total_seconds() <= 3600 * 6:
            return interval_choice.AN_HOUR_AGO
        elif interval.total_seconds() <= 3600 * 24:
            return interval_choice.SIX_HOURS_AGO
        elif interval.days < 2:
            return interval_choice.A_DAYS_AGO
        elif interval.days < 10:
            return interval_choice.TWO_DAYS_AGO
        elif interval.days < 30:
            return interval_choice.TEN_DAYS_AGO
        else:
            return interval_choice.A_MONTH_AGO


class ProductDemandPhoto(models.Model):
    dmid = models.ForeignKey(
        ProductDemand,
        on_delete=models.SET_NULL,
        related_name="demand_photo",
        db_index=True,
        null=True,
        blank=True,
    )
    demand_photo = models.ImageField(upload_to=settings.UPLOAD_DEMAND_PHOTO)
    demand_photo_snapshot = models.FilePathField(null=True, blank=True)
    inuse = models.BooleanField(default=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    photo_desc = models.CharField(max_length=255)

    def __unicode__(self):
        return self.photo_desc
