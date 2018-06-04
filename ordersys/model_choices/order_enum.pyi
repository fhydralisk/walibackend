from base.util.field_choice import FieldChoice


# TODO: Translate codes into verbose names and identifiers!

class _OStatusChoice(FieldChoice):
    WAIT_EARNEST = None
    WAIT_EARNEST_CHECK = None
    WAIT_PRODUCT_DELIVER = None
    WAIT_PRODUCT_CONFIRM = None
    WAIT_PRODUCT_CHECK = None
    WAIT_ADJUSTMENT = None
    WAIT_FINAL_PAYMENT = None
    WAIT_ADJUSTMENT_CONFIRM = None
    WAIT_ADJUSTMENT_COMPLETE = None
    WAIT_DEFAULT_ADJUSTMENT_COMPLETE = None
    WAIT_LIQUIDATE = None
    CLOSED = None
    WAIT_RECEIPT = None
    WAIT_RECEIPT_CHECK = None
    SUCCEEDED = None


class _OBuyerActionChoice(FieldChoice):
    BUYER_PAY_EARNEST = None
    BUYER_CHECK_PRODUCT = None
    BUYER_CHECK_RESULT_BAD = None
    BUYER_CHECK_RESULT_GOOD = None
    BUYER_SUBMIT_PROTOCOL = None
    BUYER_CONFIRMED_RECEIPT = None


class _OSellerActionChoice(FieldChoice):
    SELLER_SUBMIT_LOGISTICS_INFO = None
    SELLER_AGREE_PROTOCOL = None
    SELLER_REJECT_PROTOCOL = None
    SELLER_APPEND_RECEIPT_LOGISTICS = None


class _OPTypeChoice(FieldChoice):
    CANCEL = None
    ADJUST_PRICE = None
    NORMAL = None


class _PStatusChoice(FieldChoice):
    CREATED = None
    AGREED = None
    REJECTED = None
    CANCELED = None
    EXECUTED = None


class _POperateStatusChoice(FieldChoice):
    CANCEL_WAIT_RETURN = None
    CANCEL_WAIT_CONFIRM = None
    CANCEL_WAIT_REFUND = None
    CANCEL_OK = None
    ADJUST_WAIT_FINAL = None
    ADJUST_CHECK_FINAL = None
    ADJUST_CHECK_EARNEST = None
    ADJUST_OK = None
    NORMAL_WAIT_FINAL = None
    NORMAL_CHECK_FINAL = None
    NORMAL_OK = None


class _OPBuyerActionChoice(FieldChoice):
    CANCEL_APPEND_LOGISTICS_INFO = None
    BUYER_PAY_FINAL = None


class _OPSellerActionChoice(FieldChoice):
    CANCEL_CONFIRM_PRODUCT = None


class _OPFeedbackChoice(FieldChoice):
    CANCEL_FINISH = None
    ADJUST_FINISH = None
    NORMAL_FINISH = None


class _OTypeChoice(FieldChoice):
    PROCEEDING = None
    SUCCEEDED = None
    CLOSED = None
# Platform Actions on Protocol and Order...


class _OPPlatformActionChoice(FieldChoice):
    PLATFORM_CONFIRM_PAYMENT = None
    PLATFORM_CONFIRM_REFUND = None


class _ChangeTypeChoice(FieldChoice):
    REFUND_EARNEST = None
    ADJUST_FINAL = None


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
