from base.util.field_choice import FieldChoice


class _SignStatusChoice(FieldChoice):
    NOT_SIGNED = None
    ACCEPTED = None
    REJECTED = None


class _SignMethodChoice(FieldChoice):
    ACCEPT = None
    REJECT = None


sign_status_choice = _SignStatusChoice()
sign_method_choice = _SignMethodChoice()
