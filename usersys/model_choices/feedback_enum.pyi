from base.util.field_choice import FieldChoice# coding=utf-8



class _HandleChoice(FieldChoice):
    HANDLE_NONE = None
    HANDLE_CONFIRM = None
    HANDLE_REJECT = None


handle_choice = _HandleChoice()
