from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from coresys.models import CoreDistributionMethod
from .order import OrderInfo
from .distribution_enum import l_type_choice
from django.core.validators import MinValueValidator


class OrderLogisticsInfo(models.Model):
    oid = models.ForeignKey(
        OrderInfo,
        on_delete=models.CASCADE,
        related_name="order_logistics",
        verbose_name=_("order")
    )
    dmid = models.ForeignKey(
        CoreDistributionMethod,
        on_delete=models.PROTECT,
        verbose_name=_("Distribution Method")
    )
    l_type = models.IntegerField(_("logistics type"), choices=l_type_choice.choice)
    logistics_company = models.CharField(max_length=125)
    logistics_no = models.CharField(max_length=125)
    car_no = models.CharField(max_length=63)
    contact = models.CharField(max_length=100)
    contact_pn = models.CharField(max_length=50)
    attach_datetime = models.DateTimeField(auto_now_add=True)
    delivery_days = models.IntegerField(validators=[MinValueValidator(0)])

    def __unicode__(self):
        return self.logistics_company + " " + self.logistics_no
