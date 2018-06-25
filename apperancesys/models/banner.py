from django.db import models
from django.conf import settings


class Banner(models.Model):
    image = models.ImageField(upload_to=settings.UPLOAD_APPEARANCE_BANNER)
    upload_date = models.DateTimeField(auto_now_add=True)
    in_use = models.BooleanField(default=True)
