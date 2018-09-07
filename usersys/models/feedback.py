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
        verbose_name=_("用户"),
    )

    wechat_id = models.CharField(max_length=255,verbose_name='微信号')
    feedback_date = models.DateTimeField(auto_now_add=True,verbose_name='反馈日期')
    content = models.TextField(verbose_name='具体内容')
    handle = models.IntegerField(
        verbose_name=_("处理结果"),
        choices=handle_choice.choice,
        default=handle_choice.HANDLE_NONE
    )
    reward = models.FloatField(verbose_name='奖金')

    class Meta:
        verbose_name = _('用户反馈')
        verbose_name_plural = verbose_name
