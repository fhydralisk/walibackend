from base.util.field_choice import FieldChoice# -*- coding: UTF-8 -*-




class _PhotoTypeChoice(FieldChoice):
    RECEIPT_FORWARD = None
    RECEIPT_CHECK = None
    RECEIPT_RETURN = None


photo_type_choice = _PhotoTypeChoice()
