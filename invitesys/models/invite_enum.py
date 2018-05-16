from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _IStatusChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (0, _("Invite started"), "STARTED"),
        (1, _("Invitee confirmed"), "CONFIRMED"),
        (2, _("Contract signed"), "SIGNED"),
        (3, _("Cancelled by inviter"), "CANCELED"),
        (4, _("Rejected by invitee"), "REJECTED"),
        (5, _("Contract did not meet an agreement"), "CONTRACT_NOT_AGREE"),
    )


class _TInviteChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _(""), "PROCEEDING_INVITES_MINE"),
        (2, _(""), "CLOSED_INVITES_MINE"),
        (3, _(""), "PROCEEDING_INVITES_OTHERS"),
        (4, _(""), "CLOSED_INVITES_OTHERS"),
        (5, _(""), "FINISHED_INVITES_MINE"),
        (6, _(""), "FINISHED_INVITES_OTHERS"),
    )


class _HandleMethodChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _(""), "ACCEPT"),
        (2, _(""), "REJECT"),
        (3, _(""), "CANCEL"),
    )


i_status_choice = _IStatusChoice()
t_invite_choice = _TInviteChoice()
handle_method_choice = _HandleMethodChoice()
