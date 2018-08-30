# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from usersys.models import UserFeedback


class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'wechat_id', 'reward', 'content', 'handle', 'feedback_date')
    list_display_links = ('id', 'uid')
    list_editable = ('handle', )
    date_hierarchy = 'feedback_date'
    search_fields = ('uid__pn', )


to_register = [
    (UserFeedback, UserFeedbackAdmin),
]
