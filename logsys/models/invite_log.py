from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from usersys.models import UserBase
from simplified_invite.model_choices.invite_enum import i_status_choice
from simplified_invite.models import InviteInfo


class LogInviteStatus(models.Model):
    ivid = models.ForeignKey(
        InviteInfo,
        verbose_name=_("Invite"),
        related_name="invite_log",
        on_delete=models.CASCADE,
    )
    operator = models.ForeignKey(
        UserBase,
        blank=True,
        null=True,
    )
    log_date_time = models.DateTimeField(auto_now_add=True)
    i_status = models.IntegerField(choices=i_status_choice.choice)
    context = models.TextField(blank=True, null=True)
