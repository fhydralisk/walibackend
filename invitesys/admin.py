from django.contrib import admin

from invitesys.models import InviteInfo, InviteCancelReason, \
    InviteProductPhoto

class InvitePhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'invite_photo', 'photo_desc')

admin.site.register(InviteProductPhoto, InvitePhotoAdmin)
