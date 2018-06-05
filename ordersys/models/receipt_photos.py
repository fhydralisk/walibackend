from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.conf import settings
from ordersys.model_choices.photo_enum import photo_type_choice
from . import OrderInfo


class OrderReceiptPhotos(models.Model):
    oid = models.ForeignKey(
        OrderInfo,
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name="order_receipt_photos"
    )
    photo_type = models.IntegerField(choices=photo_type_choice.choice)
    update_datetime = models.DateTimeField(auto_now_add=True)
    path = models.ImageField(upload_to=settings.UPLOAD_ORDER_PHOTO)
    in_use = models.BooleanField(default=True)
