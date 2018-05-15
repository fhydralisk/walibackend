from base.util.field_choice import FieldChoice


class _RoleChoice(FieldChoice):
    BUYER = None
    SELLER = None


class _TUserChoice(FieldChoice):
    ENTERPRISE_USER = None
    INDIVIDUAL_USER = None


class _ValidateStatusChoice(FieldChoice):
    NOT_COMMITTED = None
    NOT_PROCEEDED = None
    ACCEPTED = None
    REJECTED = None


class _TPhotoChoice(FieldChoice):
    LICENSE = None
    ID_TOP = None
    ID_BOTTOM = None


role_choice = _RoleChoice()
t_user_choice = _TUserChoice()
validate_status_choice = _ValidateStatusChoice()
t_photo_choice = _TPhotoChoice()
