from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from .invite import InviteInfo
from .contract_enum import sign_status_choice


class InviteContractTemplate(models.Model):
    contract_desc = models.CharField(max_length=200)
    upload_date = models.DateTimeField(auto_now_add=True)
    path = models.FilePathField()
    in_use = models.BooleanField(default=True)

    def __unicode__(self):
        return self.contract_desc


class InviteContractSign(models.Model):
    ctid = models.ForeignKey(InviteContractTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    ivid = models.OneToOneField(InviteInfo, on_delete=models.CASCADE)
    path = models.FilePathField()
    generate_date = models.DateTimeField(auto_now_add=True)
    sign_status_A = models.IntegerField(_("Party A sign status"), choices=sign_status_choice.choice)
    sign_status_B = models.IntegerField(_("Party B sign status"), choices=sign_status_choice.choice)

    def __unicode__(self):
        return self.generate_date
