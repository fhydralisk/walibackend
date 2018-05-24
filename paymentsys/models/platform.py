from django.db import models


class PaymentPlatform(models.Model):
    description = models.TextField()
    module = models.CharField(max_length=256)
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description
