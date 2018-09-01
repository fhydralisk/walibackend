# coding=utf-8
from __future__ import unicode_literals

from base.util.field_choice import FieldChoice
from django.utils.translation import ugettext_lazy as _


class _TAppraisalChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _(""), "PROCEEDING"),
        (1, _(""), "COMPLETED"),
        (2, _(""), "CANCELED"),
     )


class _AStatusChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (2, _("买家已填写鉴定情况"), "APPRAISAL_SUBMITTED"),
        (3, _("平台审核无误"), "CONFIRMED"),
        (4, _("平台审核发现错误,需要进一步确认"), "WAIT_CONFIRMED"),
    )


t_appraisal_choice = _TAppraisalChoice()
a_status_choice = _AStatusChoice()
