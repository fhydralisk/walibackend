from base.util.field_choice import FieldChoice


class _ReceiptTypeChoice(FieldChoice):
    EARNEST_PAYMENT = None
    EARNEST_REFUND = None
    FINAL_PAYMENT = None
    FINAL_REFUND = None


class _ReceiptStatusChoice(FieldChoice):
    NOT_PAYED_WAIT_PLATFORM = None
    WAIT_PAYMENT = None
    WAIT_CHECK = None
    PAYED = None
    WAIT_REFUND = None
    REFUNDED = None
    CANCELED = None
    INVALID_RECEIPT = None


receipt_type_choice = _ReceiptTypeChoice()
receipt_status_choice = _ReceiptStatusChoice()
