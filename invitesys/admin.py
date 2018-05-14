from django.contrib import admin

from invitesys.models import InviteContractTemplate, InviteContractSign, InviteInfo

# Register your models here.
admin.site.register([InviteContractTemplate, InviteContractSign, InviteInfo])

