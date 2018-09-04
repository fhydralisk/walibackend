# coding=utf-8
from __future__ import unicode_literals

from base.util.field_choice import FieldChoice
from django.utils.translation import ugettext_lazy as _


class _TAppraisalChoice(FieldChoice):
    PROCEEDING = None
    COMPLETED = None
    CANCELED = None

class _AStatusChoice(FieldChoice):
    APPRAISAL_SUBMITTED = None
    CONFIRMED = None
    WAIT_CONFIRMED = None

t_appraisal_choice = _TAppraisalChoice()
a_status_choice = _AStatusChoice()
