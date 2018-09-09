from django.contrib import admin
from .models import LogOrderProtocolStatus, LogOrderStatus, LogInviteStatus

# Register your models here.

admin.site.register([LogOrderProtocolStatus, LogOrderStatus, LogInviteStatus])
