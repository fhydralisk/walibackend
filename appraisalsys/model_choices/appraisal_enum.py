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


class _ChangeChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("买家提交"), "BUYER_SUBMIT"),
        (1, _("买家要求修改"), "BUYER_REQUEST"),
        (2, _("其他"), "OTHER"),
    )


class _TemplateChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("废纸模板"), "PAPER"),
        (2, _("废铁模板"), "IRON"),
        (3, _("PET模版"), "PET")
    )


t_appraisal_choice = _TAppraisalChoice()
a_status_choice = _AStatusChoice()
change_reason_choice = _ChangeChoice()
template_choice = _TemplateChoice()
