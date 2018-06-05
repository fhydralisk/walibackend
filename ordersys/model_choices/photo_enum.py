# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _PhotoTypeChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("发货单"), "RECEIPT_FORWARD"),
        (2, _("验货单"), "RECEIPT_CHECK"),
        (3, _("退货单"), "RECEIPT_RETURN"),
    )


photo_type_choice = _PhotoTypeChoice()
