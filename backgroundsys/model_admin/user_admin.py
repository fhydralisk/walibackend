# coding=utf-8
from django.contrib import admin
import usersys.models as usersys
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from functools import update_wrapper
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect


class UserValidateAreaInline(admin.TabularInline):
    model = usersys.UserValidateArea
    extra = 0


class UserAdmin(admin.ModelAdmin):
    # list_filter = ('t_user',)
    # list_editable = ('is_staff', 'email',)
    list_per_page = 10
    # ordering = ('uid',)
    # fk_fields = ('machine_room_id',)#显示外键
    # search_fields = ('company',)  # 搜索字段
    # date_hierarchy = 'register_date'  # 详细时间分层筛选　


class UserValidateAdmin(UserAdmin):
    list_display = ('uid', 'phonenum', 't_user', 'contact', 'company', 'operate')
    search_fields = ('company',)
    list_filter = ('t_user',)

    def operate(self, obj):
        """自定义一个操作标签，跳转url"""
        detail = "详情"
        detail_url = reverse('backgroundsys:usersys_uservalidate_change', args=(obj.id,)) + '?status=1'
        authenticate = "认证"
        authenticate_url = reverse('backgroundsys:usersys_uservalidate_change', args=(obj.id,)) + '?status=2'
        invite = '邀请'
        invite_url = reverse('backgroundsys:invitesys_inviteinfo_changelist') + '?q={}'.format(obj.uid.pn)
        deal = '交易'
        deal_url = reverse('backgroundsys:ordersys_orderinfo_changelist') + '?q={}'.format(obj.uid.pn)

        return format_html(
            '<a href="{}">{}</a> &emsp; <a href="{}">{}</a> &emsp; <a href="{}">{}</a> &emsp; <a href="{}">{}</a>'.format(
                detail_url, detail, authenticate_url, authenticate, invite_url, invite, deal_url, deal))

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

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        def pass_view(self, userid):
            temp = usersys.UserValidate.objects.get(id=userid)
            temp.validate_status = 2
            temp.save()
            redirect_url = reverse('backgroundsys:usersys_uservalidate_change', args=(userid,)) + '?status=2'
            return HttpResponseRedirect(redirect_url)

        def fail_view(self, userid):
            temp = usersys.UserValidate.objects.get(id=userid)
            temp.validate_status = 4
            temp.save()
            redirect_url = reverse('backgroundsys:usersys_uservalidate_change', args=(userid,)) + '?status=2'
            return HttpResponseRedirect(redirect_url)

        urlpatterns = [
            url(r'^$', wrap(self.changelist_view), name='%s_%s_changelist' % info),
            url(r'^(.+)/pass', pass_view, name='%s_%s_pass' % info),
            url(r'^(.+)/fail', fail_view, name='%s_%s_fail' % info),
            url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info),
            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', wrap(self.change_view), name='%s_%s_change' % info),
            # For backwards compatibility (was the change url before 1.9)
            url(r'^(.+)/$', wrap(RedirectView.as_view(
                pattern_name='%s:%s_%s_change' % ((self.admin_site.name,) + info)
            ))),
        ]
        return urlpatterns

    def image(self, obj):
        return format_html('<img src="%s" />' % obj.validate_photo.v_photo)

    image.short_description = '经营执照'

    def button(self, obj):
        pass_url = reverse('backgroundsys:usersys_uservalidate_pass', args=(obj.id,))
        pass_des = '通过认证'
        fail_url = reverse('backgroundsys:usersys_uservalidate_fail', args=(obj.id,))
        fail_des = "拒绝认证"
        return format_html(
            '<a href="{}">{}</a> &emsp; &emsp;&emsp;&emsp;<a href="{}">{}</a>'.format(pass_url, pass_des,fail_url,fail_des))

    button.short_description = '操作'

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
                        ('texno'),
                        ('address'), ('image'), ("area"), ("validate_status"), ('button',))
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
                                    'texno', 'address', 'area', 'button','validate_status')
        return self.readonly_fields


class UserValidateAreaAdmin(UserAdmin):
    list_display = ('vid', 'pid', 'cid', 'aid')
    change_form_template = 'admin/area.html'


to_register = [
    (usersys.UserValidate, UserValidateAdmin),
    (usersys.UserValidateArea, UserValidateAreaAdmin),
]
