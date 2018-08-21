# coding=utf-8
from django.contrib import admin
import usersys.models as usersys
import parameter as para
from django.utils.html import format_html


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
        detail_url = para.admin_URL + 'usersys/uservalidate/{}/change/?id=1'.format(obj.id)
        authenticate = "认证"
        authenticate_url = para.admin_URL + 'usersys/uservalidate/{}/change/?id=2'.format(obj.id)
        invite = '邀请'
        invite_url = para.admin_URL + 'invitesys/inviteinfo/?q={}'.format(obj.uid.pn)
        deal = '交易'
        deal_url = para.admin_URL + 'ordersys/orderinfo/?q={}'.format(obj.uid.pn)

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

    def image(self, obj):
        return format_html('<img src="%s" />' % obj.validate_photo.v_photo)

    image.short_description = '经营执照'

    # @eel.expose
    def my_python(self):
        return 1

    def button(self, obj):
        return format_html(
            '<button onclick="alert(\'haha\')">你好</button>')

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
        if (get.get("id") == "1"):
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
        if (get.get("id") == "1"):
            self.readonly_fields = ('uid', 'phonenum',)
            self.inlines = []
        else:
            self.readonly_fields = ('t_user', 'image', 'company', 'contact', 'bankcard', 'obank', 'uid', 'phonenum',
                                    'texno', 'address', 'area', 'button')
        return self.readonly_fields


class UserValidateAreaAdmin(UserAdmin):
    list_display = ('vid', 'pid', 'cid', 'aid')
    change_form_template = 'admin/area.html'


to_register = [
    (usersys.UserValidate, UserValidateAdmin),
    (usersys.UserValidateArea, UserValidateAreaAdmin),
]
