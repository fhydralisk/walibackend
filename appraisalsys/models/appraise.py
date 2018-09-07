# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.conf import settings
from usersys.models import UserBase
from simplified_invite.models import InviteInfo
from appraisalsys.model_choices.appraisal_enum import a_status_choice
from demandsys.models.product import ProductTypeL1


class AppraisalInfo(models.Model):

    ivid = models.OneToOneField(
        InviteInfo,
        verbose_name=_("appraisal"),
        on_delete=models.CASCADE,
        related_name="appraisal"
    )
    a_status = models.IntegerField(_("反馈填写情况"), choices=a_status_choice.choice)
    in_accordance = models.BooleanField(_("是否符合描述"))

    parameter = models.TextField(null=True)


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


class JsonSchemaOfAppraisal(models.Model):
    t1id = models.ForeignKey(
        ProductTypeL1,
        on_delete=models.CASCADE,
        related_name="json_schema_of_appraisal",
    )
    json_schema = models.TextField()
