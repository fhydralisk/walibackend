# coding=utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


# TODO: Translate codes into verbose names and identifiers!

class _OStatusChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (3, _("等待卖家发货"), "WAIT_PRODUCT_DELIVER"),
        (4, _("卖家已发货，等待买家确认"), "WAIT_PRODUCT_CONFIRM"),
        (5, _("买家已确认收货，等待验货"), "WAIT_PRODUCT_CHECK"),
        (8, _("买家已提交变更协议，等待卖家确认"), "WAIT_ADJUSTMENT_CONFIRM"),
        (9, _("变更协议已被卖家确认，等待变更协议执行完毕"), "WAIT_ADJUSTMENT_COMPLETE"),
        (11, _("协议已达成，等待平台清算"), "WAIT_LIQUIDATE"),
        (16, _("交易关闭"), "CLOSED"),
        (21, _("订单完成"), "SUCCEEDED"),
    )


class _OBuyerActionChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (5, _(""), "BUYER_CHECK_PRODUCT"),
        (6, _(""), "BUYER_CHECK_RESULT_BAD"),
        (7, _(""), "BUYER_CHECK_RESULT_GOOD"),
        (8, _(""), "BUYER_SUBMIT_PROTOCOL"),
        (20, _(""), "BUYER_CONFIRMED_RECEIPT"),
    )


class _OSellerActionChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (4, _(""), "SELLER_SUBMIT_LOGISTICS_INFO"),
        (9, _(""), "SELLER_AGREE_PROTOCOL"),
        (10, _(""), "SELLER_REJECT_PROTOCOL"),
        (19, _(""), "SELLER_APPEND_RECEIPT_LOGISTICS"),
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
        (200, _("Adjust price protocol is executing, waiting for final payment"), "ADJUST_WAIT_FINAL"),
        (201, _("Final payment is paid, waiting for platform to transfer the payment"), "ADJUST_CHECK_FINAL"),
        (22, _("All payment has transferred by platform"), "ADJUST_OK"),
        (30, _("Normal protocol is executing, waiting for final payment from buyer"), "NORMAL_WAIT_FINAL"),
        (31, _("Final payment has been paid by buyer, waiting for platform to check"), "NORMAL_CHECK_FINAL"),
        (32, _("All payment has transferred by platform"), "NORMAL_OK"),
    )


class _OPBuyerActionChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (10, _(""), "CANCEL_APPEND_LOGISTICS_INFO"),
        (1, _(""), "BUYER_PAY_FINAL"),
    )


class _OPSellerActionChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (11, _(""), "CANCEL_CONFIRM_PRODUCT"),
    )


class _OPFeedbackChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (13, _(""), "CANCEL_FINISH"),
        (22, _(""), "ADJUST_FINISH"),
        (32, _(""), "NORMAL_FINISH"),
    )


class _OTypeChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _(""), "PROCEEDING"),
        (2, _(""), "SUCCEEDED"),
        (4, _(""), "CLOSED"),
    )
# Platform Actions on Protocol and Order...


class _OPPlatformActionChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (9000, _(""), "PLATFORM_CONFIRM_PAYMENT"),
        (9001, _(""), "PLATFORM_CONFIRM_REFUND"),
    )


class _ChangeTypeChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (2, _(""), "ADJUST_FINAL"),
    )


o_status_choice = _OStatusChoice()
op_type_choice = _OPTypeChoice()
p_status_choice = _PStatusChoice()
p_operate_status_choice = _POperateStatusChoice()
o_buyer_action_choice = _OBuyerActionChoice()
o_seller_action_choice = _OSellerActionChoice()
op_buyer_action_choice = _OPBuyerActionChoice()
op_seller_action_choice = _OPSellerActionChoice()
opf_feedback_choice = _OPFeedbackChoice()
op_platform_action_choice = _OPPlatformActionChoice()
order_type_choice = _OTypeChoice()
change_type_choice = _ChangeTypeChoice()
