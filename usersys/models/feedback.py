# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from . import UserBase
from usersys.model_choices.feedback_enum import handle_choice


class UserFeedback(models.Model):
    uid = models.ForeignKey(
        UserBase,
        on_delete=models.CASCADE,
        related_name="feedback",
        verbose_name=_("User"),
    )

    wechat_id = models.CharField(max_length=255)
    feedback_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    handle = models.IntegerField(
        verbose_name=_("处理结果"),
        choices=handle_choice.choice,
        default=handle_choice.HANDLE_NONE
    )
    reward = models.FloatField()
