# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from usersys.models import UserFeedback
from django.contrib import admin
import usersys.models as usersys
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from simple_history.admin import SimpleHistoryAdmin
from functools import update_wrapper
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect


class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'wechat_id', 'reward', 'content', 'handle', 'feedback_date')
    list_display_links = ('id', 'uid')
    list_editable = ('handle',)
    date_hierarchy = 'feedback_date'
    search_fields = ('uid__pn',)


class UserAddressBookAdmin(admin.ModelAdmin):
    list_display = ('uid', 'aid', 'street', 'contacts', 'phone')

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('uid',)
        return self.readonly_fields


class UserValidateAreaInline(admin.TabularInline):
    model = usersys.UserValidateArea
    extra = 0


class UserAdmin(SimpleHistoryAdmin):
    list_per_page = 30


class UserValidateAdmin(UserAdmin):
    list_display = ('uid', 'phonenum', 't_user', 'contact', 'company', 'validate_status', 'operate',)
    search_fields = ('company',)
    list_filter = ('t_user',)
    list_editable = ('validate_status',)
    history_list_display = ['company', 'change_reason', 'change_comment', 'validate_status', ]

    def operate(self, obj):
        """自定义一个操作标签，跳转url"""
        detail = "详情"
        detail_url = reverse('backgroundsys:usersys_uservalidate_change', args=(obj.id,)) + '?status=1'
        authenticate = "认证"
        authenticate_url = reverse('backgroundsys:usersys_uservalidate_change', args=(obj.id,)) + '?status=2'
        invite = '历史'
        invite_url = reverse('backgroundsys:usersys_uservalidate_history', args=(obj.id,))

        return format_html(
            '<a href="{}">{}</a> &emsp; <a href="{}">{}</a> &emsp; <a href="{}">{}</a>'.format(
                detail_url, detail, authenticate_url, authenticate, invite_url, invite))

    operate.short_description = '操作'

    def validate_area(self, obj):
        areas = usersys.UserValidateArea.objects.filter(vid=obj.id)
        areas_strings = ""
        for area in areas:
            area_pid = area["pid"]
            area_cid = area["cid"]
            area_aid = area["aid"]
            if area_pid:
                areas_strings += str(area_pid)
            if area_cid:
                areas_strings += str(area_cid)
            if area_aid:
                areas_strings += str(area_aid)
            areas_strings += "    "
        return areas_strings

    # def get_urls(self):
    #     from django.conf.urls import url
    #
    #     def wrap(view):
    #         def wrapper(*args, **kwargs):
    #             return self.admin_site.admin_view(view)(*args, **kwargs)
    #
    #         wrapper.model_admin = self
    #         return update_wrapper(wrapper, view)
    #
    #     info = self.model._meta.app_label, self.model._meta.model_name
    #
    #     def pass_view(self, userid):
    #         temp = usersys.UserValidate.objects.get(id=userid)
    #         temp.validate_status = 2
    #         temp.save()
    #         redirect_url = reverse('backgroundsys:usersys_uservalidate_change', args=(userid,)) + '?status=2'
    #         return HttpResponseRedirect(redirect_url)
    #
    #     def fail_view(self, userid):
    #         temp = usersys.UserValidate.objects.get(id=userid)
    #         temp.validate_status = 4
    #         temp.save()
    #         redirect_url = reverse('backgroundsys:usersys_uservalidate_change', args=(userid,)) + '?status=2'
    #         return HttpResponseRedirect(redirect_url)
    #
    #     urlpatterns = [
    #         url(r'^$', wrap(self.changelist_view), name='%s_%s_changelist' % info),
    #         url(r'^(.+)/pass', pass_view, name='%s_%s_pass' % info),
    #         url(r'^(.+)/fail', fail_view, name='%s_%s_fail' % info),
    #         url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info),
    #         url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
    #         #url(r'^(.+)/simple_history/$', wrap(self.history_view), name='%s_%s_simple_history' % info),
    #         url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
    #         url(r'^(.+)/change/$', wrap(self.change_view), name='%s_%s_change' % info),
    #         # For backwards compatibility (was the change url before 1.9)
    #         url(r'^(.+)/$', wrap(RedirectView.as_view(
    #             pattern_name='%s:%s_%s_change' % ((self.admin_site.name,) + info)
    #         ))),
    #     ]
    #     return urlpatterns

    def image(self, obj):
        return format_html('<img src="%s" />' % obj.validate_photo.v_photo)

    image.short_description = '经营执照'

    # def button(self, obj):
    #     pass_url = reverse('backgroundsys:usersys_uservalidate_pass', args=(obj.id,))
    #     pass_des = '通过认证'
    #     fail_url = reverse('backgroundsys:usersys_uservalidate_fail', args=(obj.id,))
    #     fail_des = "拒绝认证"
    #     return format_html(
    #         '<a href="{}">{}</a> &emsp; &emsp;&emsp;&emsp;<a href="{}">{}</a>'.format(pass_url, pass_des, fail_url,
    #                                                                                   fail_des))
    #
    # button.short_description = '操作'

    def area(self, obj):
        area_ids = obj.validate_area.all()
        string = ''
        for area_id in area_ids:
            if area_id.pid:
                string += area_id.pid.province
            if area_id.cid:
                string += area_id.cid.city
            if area_id.aid:
                string += area_id.aid.area
            string += '     '
        return string

    area.short_description = "经营区域"

    def get_fieldsets(self, request, obj=None):
        get = request.GET
        if (get.get("status") == "1"):
            fieldsets = (
                ('基本信息', {
                    'fields': (('uid',), ('phonenum',), ('t_user',), ('company'), ('contact'),)
                }),
                ('开票信息', {
                    'fields': (('bankcard',), ('obank',), ('texno',), ('address'))
                }),
            )
        else:
            fieldsets = (
                (None, {
                    'fields': (
                        ('uid'), ('t_user'), ('phonenum'), ('contact'), ('company'), ('bankcard',), ('obank'),
                        ('texno'), ('address'), ('image'), ("area"), ("validate_status"), ('change_reason'),
                        ('change_comment'),)
                }),
            )
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        """change self.readonly_fields and self.inlines"""
        get = request.GET
        if (get.get("status") == "1"):
            self.readonly_fields = ('uid', 'phonenum',)
            self.inlines = []
        else:
            self.readonly_fields = ('t_user', 'image', 'company', 'contact', 'bankcard', 'obank', 'uid', 'phonenum',
                                    'texno', 'address', 'area', 'button',)
        return self.readonly_fields


class UserValidateAreaAdmin(UserAdmin):
    list_display = ('vid', 'pid', 'cid', 'aid')


class UserValidaPhotoAdmin(UserAdmin):
    list_display = ('vid', 'v_photo', 'upload_date', 't_photo', 'inuse')


class UserBaseAdmin(UserAdmin):
    list_display = ('id', 'pn', 'role', 'register_date', 'is_active')


class UserSidAdmin(UserAdmin):
    list_display = ('sid', 'uid', 'generate_datetime', 'expire_datetime', 'last_login', 'last_ipaddr', 'is_login')
    ordering = ('-generate_datetime',)

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = (
            'sid', 'uid', 'generate_datetime', 'expire_datetime', 'last_login', 'last_ipaddr', 'is_login')
        return self.readonly_fields


to_register = [
    (usersys.UserBase, UserBaseAdmin),
    (usersys.UserSid, UserSidAdmin),
    (usersys.UserValidatePhoto, UserValidaPhotoAdmin),
    (UserFeedback, UserFeedbackAdmin),
    (usersys.UserValidate, UserValidateAdmin),
    (usersys.UserValidateArea, UserValidateAreaAdmin),
    (usersys.UserAddressBook, UserAddressBookAdmin),
]
