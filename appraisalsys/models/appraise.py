# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.conf import settings
from usersys.models import UserBase
from simplified_invite.models import InviteInfo
from appraisalsys.model_choices.appraisal_enum import a_status_choice
from demandsys.models.product import ProductWaterContent, ProductQuality


class ImpurityContent(models.Model):
    impcdesc = models.CharField(max_length=25, verbose_name=_("Impurity Content Description"))
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.impcdesc

class AppraisalInfo(models.Model):

    ivid = models.OneToOneField(
        InviteInfo,
        verbose_name=_("appraisal"),
        on_delete=models.CASCADE,
        related_name="appraisal"
    )
    a_status = models.IntegerField(_("反馈填写情况"), choices=a_status_choice.choice)
    in_accordance = models.BooleanField(_("是否符合描述"))
    final_total_price = models.FloatField()
    description = models.TextField(null=True, default=None)
    net_weight = models.FloatField(_("净重"), null=True)
    pure_net_weight = models.FloatField(_("结算净重"), null=True)

    wcid = models.ForeignKey(ProductWaterContent, related_name="appraisal_watercontent")
    impcid = models.ForeignKey(ImpurityContent, related_name="appraisal_impurity", null=True)

    price_1 = models.FloatField(default=None, null=True)
    price_2 = models.FloatField(default=None, null=True)
    price_3 = models.FloatField(default=None, null=True)


class CheckPhoto(models.Model):
    uploader = models.ForeignKey(
        UserBase,
        verbose_name=_("photo_uploader"),
        on_delete=models.CASCADE,
        related_name='appraisal_check_photo'
    )
    apprid = models.ForeignKey(
        AppraisalInfo,
        verbose_name=_("appraisal"),
        on_delete=models.SET_NULL,
        related_name='check_photo',
        null=True,
    )
    upload_data = models.DateTimeField(auto_now_add=True)
    in_use = models.BooleanField(default=True)
    check_photo = models.ImageField(upload_to=settings.UPLOAD_CHECK_PHOTO)
