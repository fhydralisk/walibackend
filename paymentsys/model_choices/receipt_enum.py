from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from base.util.field_choice import FieldChoice


class _ReceiptTypeChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (3, _("Final payment"), "FINAL_PAYMENT"),
        (4, _("Final refund"), "FINAL_REFUND"),
    )


class _ReceiptStatusChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("Wait to chose platform"), "NOT_PAYED_WAIT_PLATFORM"),
        (1, _("Not payed"), "WAIT_PAYMENT"),
        (2, _("Payed, wait for checking"), "WAIT_CHECK"),
        (3, _("Payed, checked"), "PAYED"),
        (4, _("Wait for refund"), "WAIT_REFUND"),
        (5, _("Refund confirmed"), "REFUNDED"),
        (200, _("Canceled"), "CANCELED"),
        (400, _("Invalid receipt"), "INVALID_RECEIPT"),
    )


receipt_type_choice = _ReceiptTypeChoice()
receipt_status_choice = _ReceiptStatusChoice()
