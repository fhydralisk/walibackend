# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from usersys.models import UserBase, UserValidate
from ordersys.models import *
from ordersys.model_choices.order_enum import o_status_choice, p_operate_status_choice
from paymentsys.models import PaymentReceipt
from logsys.models import LogOrderStatus
import parameter as para


class OrderLogInline(admin.TabularInline):
    model = LogOrderStatus
    readonly_fields = ('oid', 'operator', 'log_date_time', 'o_status', 'context')
    verbose_name = "订单日志"
    verbose_name_plural = "订单日志"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = (
        'id',
        'get_buyer',
        'get_seller',
        'o_status',
        'get_current_receipt',
        'extra_action',
        # 'copy_current_data',

    )

    # fields = ('o_status', 'get_buyer_information', 'get_seller_information', 'extra_action')
    fieldsets = (
        ('订单状态', {
            'fields': (('o_status',),)
        }),
        ('用户信息', {
            'fields': (('get_buyer_information', 'get_seller_information'),)
        }),
        ('管理员操作', {
            'fields': (('extra_action',),)
        })
    )
    readonly_fields = ('get_buyer_information', 'get_seller_information', 'extra_action')
    inlines = [OrderLogInline, ]
    list_filter = ('o_status',)
    search_fields = ('ivid__uid_s__pn', 'ivid__uid_t__pn')

    def get_buyer(self, obj):
        # type: (OrderInfo) -> object
        return obj.ivid.buyer

    get_buyer.short_description = "买家"

    def get_seller(self, obj):
        # type: (OrderInfo) -> object
        return obj.ivid.seller

    get_seller.short_description = "卖家"

    @staticmethod
    def get_user_info(obj):
        # type: (UserBase) -> object
        try:
            validate_obj = obj.user_validate
        except UserValidate.DoesNotExist:
            validate_obj = None

        if validate_obj is not None:
            company = (
                validate_obj.company if validate_obj.company is not None and len(validate_obj.company) > 0 else "N/A"
            )
            contract = (
                validate_obj.contact if validate_obj.contact is not None and len(validate_obj.contact) > 0 else "N/A"
            )

            return format_html(
                "<table>"
                "<tr><td>用户ID</td><td>{}</td></tr>"
                "<tr><td>用户手机</td><td>{}</td></tr>"
                "<tr><td>用户角色</td><td>{}</td></tr>"
                "<tr><td>用户姓名</td><td>{}</td></tr>"
                "<tr><td>用户公司</td><td>{}</td></tr>"
                # "<tr><td><a href='{}'>协助支付定金</a></td></tr>"
                "</table>",
                obj.id,
                obj.pn,
                obj.get_role_display(),
                _(contract),
                _(company),
            )
        else:
            return format_html(
                "<table>"
                "<tr><td>用户ID</td><td>{}</td></tr>"
                "<tr><td>用户手机</td><td>{}</td></tr>"
                "<tr><td>用户角色</td><td>{}</td></tr>"
                "</table>",
                obj.id,
                obj.pn,
                obj.get_role_display(),
            )

    def get_buyer_information(self, obj):
        # type: (OrderInfo) -> object
        return self.get_user_info(obj.ivid.buyer)

    get_buyer_information.short_description = "买家信息"

    def get_seller_information(self, obj):
        # type: (OrderInfo) -> object
        return self.get_user_info(obj.ivid.seller)

    get_seller_information.short_description = "卖家信息"

    def get_current_receipt(self, obj):
        # type: (OrderInfo) -> object
        try:
            return obj.current_receipt
        except PaymentReceipt.DoesNotExist:
            return "N/A"

    get_current_receipt.short_description = "当前支付票据"

    def extra_action(self, obj):
        # type: (OrderInfo) -> object
        if obj.o_status == o_status_choice.WAIT_EARNEST_CHECK:
            try:
                return format_html(
                    '<a href="{}">协助支付定金</a> | <a href="{}">人工核验定金</a>',
                    # reverse('payment:aid-payment', args=[obj.current_receipt.id])
                    "#",
                    "#"
                )
            except PaymentReceipt.DoesNotExist:
                return "出错"

        if obj.o_status in {o_status_choice.WAIT_DEFAULT_ADJUSTMENT_COMPLETE, o_status_choice.WAIT_ADJUSTMENT_COMPLETE}:
            try:
                if obj.current_protocol.p_operate_status in {
                    p_operate_status_choice.NORMAL_CHECK_FINAL,
                    p_operate_status_choice.ADJUST_CHECK_FINAL
                }:
                    return format_html(
                        '<a href="{}">协助支付尾款</a> | <a href="{}">人工核验尾款</a>',
                        # reverse('payment:aid-payment', args=[obj.current_receipt.id])
                        "#",
                        "#"
                    )
            except (OrderProtocol.DoesNotExist, PaymentReceipt.DoesNotExist):
                return "出错"

        return "N/A"

    extra_action.short_description = "操作"

    list_display_links = ('id',)


class OrderProtocolAdmin(admin.ModelAdmin):
    # ordering = ('-id',)
    list_display = (
        'oid',
        'op_type',
        'p_operate_status',
        'c_price',
        'description',
        'reason',
        'op_datetime'
    )


class OrderLogisticsInfoAdmin(admin.ModelAdmin):
    list_display = (
        'oid',
        'dmid',
        'l_type',
        'logistics_company',
        'logistics_no',
        'car_no',
        'contact',
        'contact_pn',
        'delivery_days',
        'attach_datetime'
    )


to_register = [
    (OrderInfo, OrderAdmin),
    (OrderProtocol, OrderProtocolAdmin),
    (OrderLogisticsInfo,OrderLogisticsInfoAdmin),
]
