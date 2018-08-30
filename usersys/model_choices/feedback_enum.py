# coding=utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _HandleChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("未处理"), "HANDLE_NONE"),
        (2, _("已处理 - 认可"), "HANDLE_CONFIRM"),
        (3, _("已处理 - 不认可"), "HANDLE_REJECT")
    )


handle_choice = _HandleChoice()
