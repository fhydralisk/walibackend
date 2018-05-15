from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from usersys.models import UserBase
from demandsys.models import ProductDemand
from coresys.models import CoreDistributionMethod, CorePaymentMethod
from .invite_enum import i_status_choice
from demandsys.models.demand_enum import unit_choice


class InviteInfo(models.Model):
    uid_s = models.ForeignKey(
        UserBase,
        on_delete=models.CASCADE,
        related_name="user_invite_src",
        db_index=True,
        verbose_name=_("inviter")
    )
    uid_t = models.ForeignKey(
        UserBase,
        on_delete=models.CASCADE,
        related_name="user_invite_dst",
        db_index=True,
        verbose_name=_("invitee")
    )
    dmid_s = models.ForeignKey(
        ProductDemand,
        on_delete=models.PROTECT,  # Do not allow?
        related_name="demand_invite_src",
        verbose_name=_("inviter's demand"),
        null=True,
        blank=True
    )
    dmid_t = models.ForeignKey(
        ProductDemand,
        on_delete=models.PROTECT,
        related_name="demand_invite_dst",
        verbose_name=_("invitee's demand")
    )
    quantity = models.FloatField()
    price = models.FloatField()
    unit = models.IntegerField(max_length=unit_choice.MAX_LENGTH, choices=unit_choice.choice)
    pmid = models.ForeignKey(CorePaymentMethod, on_delete=models.PROTECT, verbose_name=_("Pay method"))
    disid = models.ForeignKey(CoreDistributionMethod, on_delete=models.PROTECT, verbose_name=_("Distribution Method"))
    dis_duration = models.IntegerField(verbose_name=_("Distribution duration"))
    i_status = models.IntegerField(_("Invite status"), choices=i_status_choice.choice)
    reason = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return str(self.uid_s) + " v.s. " + str(self.uid_t)
