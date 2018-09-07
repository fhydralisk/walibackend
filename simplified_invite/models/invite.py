# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from usersys.models import UserBase, UserAddressBook

from demandsys.models import ProductDemand
from coresys.models import CoreAddressArea
from simplified_invite.model_choices.invite_enum import i_status_choice
from usersys.model_choices.user_enum import role_choice, change_reason_choice

from simple_history.models import HistoricalRecords


class InviteCancelReason(models.Model):
    in_use = models.BooleanField(default=True, verbose_name='是否使用')
    reason = models.CharField(max_length=256, verbose_name='原因')

    class Meta:
        verbose_name = _('邀请取消原因')
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.reason


class InviteInfo(models.Model):

    def __init__(self, *args, **kwargs):
        super(InviteInfo, self).__init__(*args, **kwargs)

        self.initial_i_status = self.i_status

    class Meta:
        verbose_name = _('邀请信息')
        verbose_name_plural = verbose_name

    uid_s = models.ForeignKey(
        UserBase,
        on_delete=models.CASCADE,
        related_name="simplified_user_invite_src",
        db_index=True,
        verbose_name=_("发起人")
    )
    uid_t = models.ForeignKey(
        UserBase,
        on_delete=models.CASCADE,
        related_name="simplified_user_invite_dst",
        db_index=True,
        verbose_name=_("受邀人")
    )
    dmid_s = models.ForeignKey(
        ProductDemand,
        on_delete=models.CASCADE,  # Do not allow?
        related_name="simplified_demand_invite_src",
        verbose_name=_("发起人需求"),
        null=True,
        blank=True
    )
    dmid_t = models.ForeignKey(
        ProductDemand,
        on_delete=models.CASCADE,
        related_name="simplified_demand_invite_dst",
        verbose_name=_("受邀人需求")
    )
    quantity = models.FloatField(verbose_name='需求量/供应量')
    price = models.FloatField(verbose_name='价格')

    i_status = models.IntegerField(_("邀请状态"), choices=i_status_choice.choice)
    reason_class = models.ForeignKey(
        InviteCancelReason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='取消原因ID',
    )
    reason = models.TextField(null=True, blank=True, verbose_name='拒绝、取消原因')
    abid = models.ForeignKey(
        UserAddressBook,
        on_delete=models.SET_NULL,
        verbose_name=_("区地址"),
        related_name="simplified_invite",
        null=True,
        blank=True
    )
    aid = models.ForeignKey(CoreAddressArea, blank=True, null=True, related_name="simplified_invite",
                            verbose_name='收/发货地址')
    street = models.CharField(max_length=511, blank=True, null=True, verbose_name='具体地址')

    history = HistoricalRecords()
    change_comment = models.TextField(verbose_name='修改备注', null=True, blank=True)
    change_reason = models.CharField(verbose_name='修改原因', default='买家要求修改', max_length=100,
                                     choices=change_reason_choice.choice)

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
    def buyer_demand(self):
        if self.buyer == self.uid_s:
            return self.dmid_s
        elif self.buyer == self.uid_t:
            return self.dmid_t
        else:
            raise AssertionError("Either inviter or invitee should be buyer")

    @property
    def seller_demand(self):
        if self.seller == self.uid_s:
            return self.dmid_s
        elif self.seller == self.uid_t:
            return self.dmid_t
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
