from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


# TODO: Translate codes into verbose names and identifiers!

class _OStatusChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (1, _("Waiting for buyer to pay earnest"), "WAIT_EARNEST"),
        (2, _("Buyer paid earnest, waiting for platform to check."), "WAIT_EARNEST_CHECK"),
        (3, _("Waiting for seller to deliver"), "WAIT_PRODUCT_DELIVER"),
        (4, _("Seller has delivered, waiting for buyer's confirmation"), "WAIT_PRODUCT_CONFIRM"),
        (5, _("Buyer has got the product, waiting for checking result"), "WAIT_PRODUCT_CHECK"),
        (6, _("Product quality does not match the demand, waiting for adjustment protocol"), "WAIT_ADJUSTMENT"),
        (7, _("Protocol quality matches the demand, waiting for final payment"), "WAIT_FINAL_PAYMENT"),
        (8, _("Buyer has submitted the adjustment protocol, waiting for confirmation from seller"), "WAIT_ADJUSTMENT_CONFIRM"),
        (9, _("Adjustment protocol has been confirmed, waiting for completion"), "WAIT_ADJUSTMENT_COMPLETE"),
        (16, _("Adjustment has been completed, no receipt needed, order closed"), "CLOSED"),
        (18, _("Adjustment has been completed, waiting for seller to send receipt"), "WAIT_RECEIPT"),
        (19, _("Receipt has been send, waiting for buyer's confirmation"), "WAIT_RECEIPT_CHECK"),
        (21, _("Order succeeded"), "SUCCEEDED"),
    )


class _OPTypeChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (1, _("Cancel order"), "CANCEL"),
        (2, _("Adjust price"), "ADJUST_PRICE"),
        (3, _("Normal process"), "NORMAL"),
    )


class _PStatusChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (0, _("Protocol created"), "CREATED"),
        (1, _("Agreed by seller"), "AGREED"),
        (2, _("Rejected by seller"), "REJECTED"),
        (3, _("Canceled by buyer"), "CANCELED"),
        (4, _("Successfully executed"), "EXECUTED"),
    )


class _POperateStatusChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (10, _("Cancel protocol is executing, waiting for return of goods"), "CANCEL_WAIT_RETURN"),
        (11, _("Goods returned, waiting for confirmation"), "CANCEL_WAIT_CONFIRM"),
        (12, _("Return has been confirmed, waiting for platform to return the earnest"), "CANCEL_WAIT_REFINE"),
        (13, _("Platform has returned the earnest"), "CANCEL_OK"),
        (200, _("Adjust price protocol is executing, waiting for final payment"), "ADJUST_WAIT_FINAL"),
        (201, _("Final payment is paid, waiting for platform to transfer the payment"), "ADJUST_CHECK_FINAL"),
        (210, _("Adjust price protocol is executing, waiting for platform to return the earnest"), "ADJUST_CHECK_EARNEST"),
        (22, _("All payment has transferred by platform"), "ADJUST_OK"),
        (30, _("Normal protocol is executing, waiting for final payment from buyer"), "NORMAL_WAIT_FINAL"),
        (31, _("Final payment has been paid by buyer, waiting for platform to check"), "NORMAL_CHECK_FINAL"),
        (32, _("All payment has transferred by platform"), "NORMAL_OK"),
    )


o_status_choice = _OStatusChoice()
op_type_choice = _OPTypeChoice()
p_status_choice = _PStatusChoice()
p_operate_status_choice = _POperateStatusChoice()
