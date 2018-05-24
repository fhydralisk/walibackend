from django.contrib import admin
from paymentsys.models import PaymentReceipt, PaymentPlatform

# Register your models here.
admin.site.register([PaymentReceipt, PaymentPlatform])
