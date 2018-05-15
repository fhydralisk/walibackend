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
    CLOSED = None
    WAIT_RECEIPT = None
    WAIT_RECEIPT_CHECK = None
    SUCCEEDED = None


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
    CANCEL_WAIT_REFINE = None
    CANCEL_OK = None
    ADJUST_WAIT_FINAL = None
    ADJUST_CHECK_FINAL = None
    ADJUST_CHECK_EARNEST = None
    ADJUST_OK = None
    NORMAL_WAIT_FINAL = None
    NORMAL_CHECK_FINAL = None
    NORMAL_OK = None


o_status_choice = _OStatusChoice()
op_type_choice = _OPTypeChoice()
p_status_choice = _PStatusChoice()
p_operate_status_choice = _POperateStatusChoice()
