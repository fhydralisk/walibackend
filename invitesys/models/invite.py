from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from usersys.models import UserBase
from demandsys.models import ProductDemand
from coresys.models import CoreDistributionMethod, CorePaymentMethod
from invitesys.model_choices.invite_enum import i_status_choice
from demandsys.model_choices.demand_enum import unit_choice
from usersys.model_choices.user_enum import role_choice


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

    @property
    def buyer(self):
        if self.uid_s.role == role_choice.BUYER:
            return self.uid_s
        elif self.uid_t.role == role_choice.BUYER:
            return self.uid_t
        else:
            raise AssertionError("Either inviter or invitee should be buyer")

    @property
    def seller(self):
        if self.uid_s.role == role_choice.SELLER:
            return self.uid_s
        elif self.uid_t.role == role_choice.SELLER:
            return self.uid_t
        else:
            raise AssertionError("Either inviter or invitee should be seller")

    @property
    def total_price(self):
        return self.price * self.quantity

    @property
    def earnest(self):
        return self.total_price * self.pmid.deposit_scale

    @property
    def final_price(self):
        return self.total_price - self.earnest
