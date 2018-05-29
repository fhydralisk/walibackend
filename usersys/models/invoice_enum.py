# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _InvoiceTypeChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("普通发票 - 个人"), "COMMON_INDIVIDUAL"),
        (2, _("普通发票 - 公司"), "COMMON_COMPANY"),
        (3, _("增值税专用发票"), "VALUE_ADDED_SPECIAL")
    )


invoice_type_choice = _InvoiceTypeChoice()
