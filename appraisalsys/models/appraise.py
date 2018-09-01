# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from invitesys.models import InviteInfo
from appraisalsys.model_choices.appraisal_enum import a_status_choice


class AppraisalInfo(models.Model):

    ivid = models.OneToOneField(
        InviteInfo,
        verbose_name=_("appraisal"),
        on_delete=models.CASCADE,
        related_name="appraisal"
    )
    a_status = models.IntegerField(_("反馈填写情况"), choices=a_status_choice.choice)
    # TODO other fields