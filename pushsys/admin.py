from django.contrib import admin
import models
import pushsys.funcs.push  # Don't remove, for trigger.


# Register your models here.
admin.site.register([models.JPushSecret, models.PushTemplate])
