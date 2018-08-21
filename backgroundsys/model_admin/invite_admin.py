# coding=utf-8
from django.contrib import admin
import invitesys.models as invitesys
from usersys.models import UserBase, UserValidate
import parameter as para
from django.utils.html import format_html


#
# class UserValidateAreaInline(admin.TabularInline):
#     model = usersys.UserValidateArea
#     extra = 0
#
#
# class UserValidatePhotoInline(admin.TabularInline):
#     model = usersys.UserValidatePhoto
#     extra = 0


class InviteAdmin(admin.ModelAdmin):
    list_per_page = 10


class InviteCancelReasonAdmin(InviteAdmin):
    list_display = (
        'id',
        'in_use',
        'reason',
    )

class InviteInfoAdmin(InviteAdmin):
    list_display = (
        'id', 'buyer_company', 'pn', 'kind', 'standard', 'quantity_unit', 'price_unit', 'i_status', 'operate')
    search_fields = ('uid_s__pn', 'uid_t__pn')

    def pn(self, obj):
        if obj.uid_s.role == 1:
            buyer = obj.uid_s
        else:
            buyer = obj.uid_t
        return buyer.pn

    pn.short_description = "买方电话"

    def get_list_display(self, request):
        return self.list_display

    def buyer_company(self, obj):
        if obj.uid_s.role == 1:
            buyer = obj.uid_s
        else:
            buyer = obj.uid_t
        return buyer.user_validate.company

    buyer_company.short_description = "买方"

    def kind(self, obj):
        # FIXME inviter's or invitee's
        try:
            t3 = obj.dmid_t.qid.t3id
            t2 = t3.t2id
            t1 = t2.t1id
            string = t1.tname1 + '-' + t2.tname2 + '-' + t3.tname3
        except:
            string = ' - '
        return string

    kind.short_description = '品类'

    def standard(self, obj):
        # FIXME inviter's or invitee's
        try:
            string = obj.dmid_t.qid.pqdesc
        except:
            string = ' - '
        return string

    standard.short_description = '标准'

    def quantity_unit(self, obj):
        try:
            string = str(obj.quantity)
            if obj.unit == 1:
                string += "吨"
            else:
                string += "千克"
        except:
            string = ' - '
        return string

    quantity_unit.short_description = '数量'

    def price_unit(self, obj):
        try:
            string = str(obj.price)
            if obj.unit == 1:
                string += "/吨"
            else:
                string += "/千克"
        except:
            string = ' - '
        return string

    price_unit.short_description = '单价'

    def operate(self, obj):
        address = para.admin_URL + 'invitesys/inviteinfo/{}'.format(obj.id)
        title = "详情"
        return format_html('<a href="{}">{}</a>'.format(address, title))

    operate.short_description = '操作'


to_register = [
    (invitesys.InviteInfo, InviteInfoAdmin),
    (invitesys.InviteCancelReason,InviteCancelReasonAdmin),
]
