from django.contrib import admin
from backgroundsys.admin_site import admin_site
from invitesys.models import InviteContractTemplate, InviteContractSign, InviteInfo, InviteCancelReason, \
    InviteProductPhoto


# Register your models here.


class InvitePhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'invite_photo', 'photo_desc')


admin_site.register(InviteProductPhoto, InvitePhotoAdmin)
