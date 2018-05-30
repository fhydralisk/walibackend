from django.contrib import admin

from invitesys.models import InviteContractTemplate, InviteContractSign, InviteInfo, InviteCancelReason

# Register your models here.
admin.site.register([InviteContractTemplate, InviteContractSign, InviteInfo, InviteCancelReason])

