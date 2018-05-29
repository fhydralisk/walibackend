from base.util.field_choice import FieldChoice# -*- coding: UTF-8 -*-




class _InvoiceTypeChoice(FieldChoice):
    COMMON_INDIVIDUAL = None
    COMMON_COMPANY = None
    VALUE_ADDED_SPECIAL = None


invoice_type_choice = _InvoiceTypeChoice()
