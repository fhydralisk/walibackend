from base.util.field_choice import FieldChoice


class _IStatusChoice(FieldChoice):
    STARTED = None
    CONFIRMED = None
    SIGNED = None
    CANCELED = None
    REJECTED = None
    CONTRACT_NOT_AGREE = None


class _TInviteChoice(FieldChoice):
    PROCEEDING_INVITES = None
    CLOSED_INVITES = None
    FINISHED_INVITES= None


class _HandleMethodChoice(FieldChoice):
    ACCEPT = None
    REJECT = None
    CANCEL = None


i_status_choice = _IStatusChoice()
t_invite_choice = _TInviteChoice()
handle_method_choice = _HandleMethodChoice()
