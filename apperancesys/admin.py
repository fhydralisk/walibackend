# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from apperancesys.models import Banner
from backgroundsys.admin_site import admin_site
# Register your models here.


admin_site.register(Banner)
