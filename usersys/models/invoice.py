from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from .usermodel import UserBase
from usersys.model_choices.invoice_enum import invoice_type_choice


class UserReceiptInfo(models.Model):
    uid = models.ForeignKey(UserBase, related_name="user_receipt", on_delete=models.CASCADE, db_index=True)
    receipt_type = models.IntegerField(
        choices=invoice_type_choice.choice
    )
    receipt_header = models.CharField(max_length=512)
    tex_identity = models.CharField(max_length=255, null=True, blank=True)
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return "Invoice Info, Header: %s" % self.receipt_header
