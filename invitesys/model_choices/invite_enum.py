# coding=utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _IStatusChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (0, _("邀请发起"), "STARTED"),
        (1, _("受邀方确认"), "CONFIRMED"),
        (2, _("合同签署完毕"), "SIGNED"),
        (3, _("发起方取消"), "CANCELED"),
        (4, _("受邀方拒绝"), "REJECTED"),
        (5, _("合同未达成"), "CONTRACT_NOT_AGREE"),
        (6, _("受邀人讨价还价"), "INVITER_NEGOTIATE"),
        (7, _("邀请人讨价还价"), "INVITEE_NEGOTIATE"),
    )


class _TInviteChoice(FieldChoice):
    CHOICE_DISPLAY = (
        # (1, _(""), "PROCEEDING_INVITES_MINE"),
        # (2, _(""), "CLOSED_INVITES_MINE"),
        # (3, _(""), "PROCEEDING_INVITES_OTHERS"),
        # (4, _(""), "CLOSED_INVITES_OTHERS"),
        # (5, _(""), "FINISHED_INVITES_MINE"),
        # (6, _(""), "FINISHED_INVITES_OTHERS"),
        (1, _(""), "PROCEEDING_INVITES"),
        (2, _(""), "CLOSED_INVITES"),
        (3, _(""), "FINISHED_INVITES"),
    )


class _HandleMethodChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _(""), "ACCEPT"),
        (2, _(""), "REJECT"),
        (3, _(""), "CANCEL"),
        (4, _(""), "NEGOTIATE"),
    )


i_status_choice = _IStatusChoice()
t_invite_choice = _TInviteChoice()
handle_method_choice = _HandleMethodChoice()
