from base.util.field_choice import FieldChoice# coding=utf-8



class _TAppraisalChoice(FieldChoice):
    PROCEEDING = None
    COMPLETED = None
    CANCELED = None


class _AStatusChoice(FieldChoice):
    APPRAISAL_SUBMITTED = None
    CONFIRMED = None
    WAIT_CONFIRMED = None


class _ChangeChoice(FieldChoice):
    BUYER_SUBMIT = None
    BUYER_REQUEST = None
    OTHER = None


class _TemplateChoice(FieldChoice):
    PET = None
    IRON = None
    PAPER = None

t_appraisal_choice = _TAppraisalChoice()
a_status_choice = _AStatusChoice()
change_reason_choice = _ChangeChoice()
template_choice = _TemplateChoice()
