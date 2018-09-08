# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig


class AppraisalConfig(AppConfig):
    name = 'appraisalsys'
    verbose_name = _("评价")
