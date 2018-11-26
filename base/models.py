from django.db import models


class PhoneValidatorMasterKey(models.Model):
    app_key = models.CharField(max_length=255)
    app_secret = models.CharField(max_length=255)
    template_code = models.CharField(max_length=255)
    sign_name = models.CharField(max_length=255)
    in_use = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
