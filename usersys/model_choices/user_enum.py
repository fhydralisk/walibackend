# coding=utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _RoleChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("Buyer"), "BUYER"),
        (2, _("Seller"), "SELLER"),
    )


class _TUserChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("企业用户"), "ENTERPRISE_USER"),
        (2, _("个人用户"), "INDIVIDUAL_USER")
    )


class _ValidateStatusChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("未提交"), "NOT_COMMITTED"),
        (1, _("未处理"), "NOT_PROCEEDED"),
        (2, _("已通过"), "ACCEPTED"),
        (4, _("已拒绝"), "REJECTED"),
    )


class _TPhotoChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("营业执照"), "LICENSE"),
        (2, _("身份证正面"), "ID_TOP"),
        (3, _("身份证背面"), "ID_BOTTOM"),
    )


role_choice = _RoleChoice()
t_user_choice = _TUserChoice()
validate_status_choice = _ValidateStatusChoice()
t_photo_choice = _TPhotoChoice()
