from base.util.field_choice import FieldChoice


class _IStatusChoice(FieldChoice):
    STARTED = None
    CONFIRMED = None
    SIGNED = None
    CANCELED = None
    REJECTED = None
    CONTRACT_NOT_AGREE = None


class _TInviteChoice(FieldChoice):
    PROCEEDING_INVITES_MINE = None
    CLOSED_INVITES_MINE = None
    PROCEEDING_INVITES_OTHERS = None
    CLOSED_INVITES_OTHERS = None
    FINISHED_INVITES_MINE = None
    FINISHED_INVITES_OTHERS = None


class _HandleMethodChoice(FieldChoice):
    ACCEPT = None
    REJECT = None
    CANCEL = None


i_status_choice = _IStatusChoice()
t_invite_choice = _TInviteChoice()
handle_method_choice = _HandleMethodChoice()
