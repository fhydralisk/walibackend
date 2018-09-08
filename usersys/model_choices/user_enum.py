# coding=utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _RoleChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("买家"), "BUYER"),
        (2, _("卖家"), "SELLER"),
    )


class _TUserChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("企业用户"), "ENTERPRISE_USER"),
        (2, _("个人用户"), "INDIVIDUAL_USER")
    )


class _ValidateStatusChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("用户尚未提交认证审核申请"), "NOT_COMMITTED"),
        (1, _("用户已提交认证审核申请，但审核尚未被处理"), "NOT_PROCEEDED"),
        (2, _("用户已提交认证审核申请，且审核已通过"), "ACCEPTED"),
        (4, _("用户已提交认证审核申请，但审核被拒绝"), "REJECTED"),
    )


class _TPhotoChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("Business license"), "LICENSE"),
        (2, _("Top side of ID card"), "ID_TOP"),
        (3, _("Bottom side of ID card"), "ID_BOTTOM"),
    )


role_choice = _RoleChoice()
t_user_choice = _TUserChoice()
validate_status_choice = _ValidateStatusChoice()
t_photo_choice = _TPhotoChoice()
