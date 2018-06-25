from django.contrib import admin

from invitesys.models import InviteContractTemplate, InviteContractSign, InviteInfo, InviteCancelReason, \
    InviteProductPhoto

# Register your models here.


class InvitePhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'invite_photo', 'photo_desc')


admin.site.register([InviteContractTemplate, InviteContractSign, InviteInfo, InviteCancelReason])
admin.site.register(InviteProductPhoto, InvitePhotoAdmin)
