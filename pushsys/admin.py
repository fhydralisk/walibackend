import sys
from django.contrib import admin
import models
from .funcs.utils.push import initialize

# Register your models here.
admin.site.register([models.JPushSecret, models.PushTemplate])

# Avoid accessing models when migrate at application start
if 'migrat' not in ''.join(sys.argv):
    initialize()
