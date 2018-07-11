# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from base.util.field_choice import FieldChoice


class _PushStateChoice(FieldChoice):
    CHOICE_DISPLAY = (
        ("orderinfo_o_status", _(""), "ORDERINFO_O_STATUS"),
        ("inviteinfo_i_status", _(""), "INVITEINFO_I_STATUS"),
    )


push_state_choice = _PushStateChoice()
