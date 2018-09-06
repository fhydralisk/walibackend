# coding=utf-8
from django.contrib import admin
import simplified_invite.models as invite
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from simple_history.admin import SimpleHistoryAdmin


class InviteInfoAdmin(SimpleHistoryAdmin):
    list_display = ('uid_s', 'uid_t', 'i_status', 'quantity', 'price', 'operate',)
    history_list_display = ['change_reason', 'change_comment', ]

    def operate(self, obj):
        detail = "详情"
        detail_url = reverse('backgroundsys:simplified_invite_inviteinfo_change', args=(obj.id,))
        history = '历史'
        history_url = reverse('backgroundsys:simplified_invite_inviteinfo_history', args=(obj.id,))

        return format_html(
            '<a href="{}">{}</a> &emsp; <a href="{}">{}</a>'.format(detail_url, detail, history_url, history))

    operate.short_description = '操作'


to_register = [
    (invite.InviteInfo, InviteInfoAdmin),
]
