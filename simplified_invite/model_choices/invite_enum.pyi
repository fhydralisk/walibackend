from base.util.field_choice import FieldChoice


class _IStatusChoice(FieldChoice):
    STARTED = None
    CONFIRMED = None
    SIGNED = None
    CANCELED = None
    REJECTED = None
    CONTRACT_NOT_AGREE = None
    INVITER_NEGOTIATE = None
    INVITEE_NEGOTIATE = None


class _TInviteChoice(FieldChoice):
        # (1, _(""), "PROCEEDING_INVITES_MINE"),
        # (2, _(""), "CLOSED_INVITES_MINE"),
        # (3, _(""), "PROCEEDING_INVITES_OTHERS"),
        # (4, _(""), "CLOSED_INVITES_OTHERS"),
        # (5, _(""), "FINISHED_INVITES_MINE"),
        # (6, _(""), "FINISHED_INVITES_OTHERS"),
    PROCEEDING_INVITES = None
    CLOSED_INVITES = None
    FINISHED_INVITES = None


class _HandleMethodChoice(FieldChoice):
    ACCEPT = None
    REJECT = None
    CANCEL = None
    NEGOTIATE = None


class _TInvite2Appraisal(FieldChoice):
    PROCEEDING = None
    COMPLETED_OR_CANCELED = None


i_status_choice = _IStatusChoice()
t_invite_choice = _TInviteChoice()
handle_method_choice = _HandleMethodChoice()
t_invite2appraisal_choice = _TInvite2Appraisal()
