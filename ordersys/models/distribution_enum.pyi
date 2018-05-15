from base.util.field_choice import FieldChoice


class _LTypeChoice(FieldChoice):
    FORWARD = None
    RETURN = None
    RECEIPT = None


l_type_choice = _LTypeChoice()
