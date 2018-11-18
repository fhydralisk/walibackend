# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

import logging
from base.util.csv_unicode_helper import UnicodeWriter
from django.contrib import admin
from django.http.response import HttpResponse
from simplified_invite.models import InviteInfo
from simplified_invite.model_choices.invite_enum import i_status_choice
from usersys.models import UserValidate
from appraisalsys.models import AppraisalInfo

logger = logging.getLogger(__name__)


class InviteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_product_type_l1',
        'get_product_type_l2',
        'get_product_type_l3',
        'get_invite_money',
        'get_confirmed_money',
        'get_username_s',
        'get_username_t',
        'i_status',
        'get_datetime',
    )
    actions = ["export_as_csv"]

    search_fields = (
        'uid_s__user_validate__company',
        'uid_t__user_validate__company',
        'uid_s__user_validate__phonenum',
        'uid_t__user_validate__phonenum',
        'uid_s__user_validate__contact',
        'uid_t__user_validate__contact',
        'uid_s__pn',
        'uid_t__pn',
        'dmid_t__pid__tname3',
        'dmid_t__pid__t2id__tname2',
        'dmid_t__pid__t2id__t1id__tname1',
    )

    list_filter = (
        'i_status',

    )
    # list_display = ('id', 'uid', 'wechat_id', 'reward', 'content', 'handle', 'feedback_date')
    # list_display_links = ('id', 'uid')
    # list_editable = ('handle', )
    # date_hierarchy = 'feedback_date'
    # search_fields = ('uid__pn', )

    # FIXME: Performance issue here, each getXXX calls database once.

    def get_product_type_l3(self, obj):
        # type: (InviteInfo) -> unicode

        return obj.dmid_t.pid.tname3
    get_product_type_l3.short_description = _("三级品类")

    def get_product_type_l2(self, obj):
        # type: (InviteInfo) -> unicode

        return obj.dmid_t.pid.t2id.tname2
    get_product_type_l2.short_description = _("二级品类")

    def get_product_type_l1(self, obj):
        # type: (InviteInfo) -> unicode

        return obj.dmid_t.pid.t2id.t1id.tname1
    get_product_type_l1.short_description = _("一级品类")

    def get_invite_money(self, obj):
        # type: (InviteInfo) -> object

        return obj.quantity * obj.price
    get_invite_money.short_description = _("邀请总金额")

    def get_confirmed_money(self, obj):
        # type: (InviteInfo) -> object

        if obj.i_status == i_status_choice.SIGNED:
            try:
                return obj.appraisal.final_total_price
            except AppraisalInfo.DoesNotExist:
                logger.warn("Appraisal does not exist corresponded to Invite with id: %d" % obj.id)
                return '-'
        else:
            return '-'
    get_confirmed_money.short_description = _("成交总金额")

    def get_company_s(self, obj):
        # type: (InviteInfo) -> unicode
        try:
            return obj.uid_s.user_validate.company
        except UserValidate.DoesNotExist:
            return "-"
    get_company_s.short_description = _("邀请人公司名称")

    def get_pn_s(self, obj):
        # type: (InviteInfo) -> unicode
        return obj.uid_s.pn
    get_pn_s.short_description = _("邀请人注册手机号")

    def get_pn_validate_s(self, obj):
        # type: (InviteInfo) -> unicode
        try:
            return obj.uid_s.user_validate.phonenum
        except UserValidate.DoesNotExist:
            return "-"
    get_pn_validate_s.short_description = _("邀请人验证电话号码")

    def get_username_s(self, obj):
        # type: (InviteInfo) -> unicode

        try:
            return obj.uid_s.user_validate.contact
        except UserValidate.DoesNotExist:
            return "-"
    get_username_s.short_description = _("邀请人用户姓名")

    def get_company_t(self, obj):
        # type: (InviteInfo) -> unicode
        try:
            return obj.uid_t.user_validate.company
        except UserValidate.DoesNotExist:
            return "-"
    get_company_t.short_description = _("受邀人公司名称")

    def get_pn_t(self, obj):
        # type: (InviteInfo) -> unicode
        return obj.uid_t.pn
    get_pn_t.short_description = _("受邀人注册手机号")

    def get_pn_validate_t(self, obj):
        # type: (InviteInfo) -> unicode
        try:
            return obj.uid_t.user_validate.phonenum
        except UserValidate.DoesNotExist:
            return "-"
    get_pn_validate_t.short_description = _("受邀人验证电话号码")

    def get_username_t(self, obj):
        # type: (InviteInfo) -> unicode

        try:
            return obj.uid_t.user_validate.contact
        except UserValidate.DoesNotExist:
            return "-"
    get_username_t.short_description = _("受邀人用户姓名")

    def get_datetime(self, obj):
        # type: (InviteInfo) -> unicode

        first_log = obj.invite_log.first()
        if first_log is not None:
            return first_log.log_date_time
        else:
            return '-'
    get_datetime.short_description = _("生成时间")

    def export_as_csv(self, request, queryset):

        def get_verbose_name_of_field_name(field_name):
            if hasattr(self.model, field_name):
                return self.model._meta.get_field(field_name).verbose_name
            elif hasattr(self, field_name):
                return getattr(getattr(self, field_name), 'short_description', '')
            else:
                return ''

        def get_value(o, f):
            if hasattr(o, f):
                return unicode(getattr(o, f))
            elif hasattr(self, f) and callable(getattr(self, f)):
                return unicode(getattr(self, f)(o))
            else:
                return '-'

        field_names = (
            'id',
            'get_product_type_l1',
            'get_product_type_l2',
            'get_product_type_l3',
            'get_invite_money',
            'get_confirmed_money',
            'get_username_s',
            'get_company_s',
            'get_pn_s',
            'get_pn_validate_s',
            'get_username_t',
            'get_company_t',
            'get_pn_t',
            'get_pn_validate_t',
            'i_status',
            'get_datetime',
        )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=invite_exported.csv'
        writer = UnicodeWriter(response)

        writer.writerow(map(get_verbose_name_of_field_name, field_names))
        for obj in queryset:
            writer.writerow([get_value(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = _("导出CSV")


to_register = [
    (InviteInfo, InviteAdmin),
]
