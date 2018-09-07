# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import appraisalsys.models as models

# Register your models here.

admin.site.register([models.AppraisalInfo, models.CheckPhoto, models.ImpurityContent, models.JsonSchemaOfAppraisal])
