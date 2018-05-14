from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models


class CorePaymentMethod(models.Model):
    ord = models.IntegerField(_("Order Number"))
    deposit_scale = models.FloatField()
    opmdesc = models.TextField(verbose_name=_("Description"), max_length=125)
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.opmdesc
