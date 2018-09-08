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
    BUYER = None
    OTHERREASON = None


t_appraisal_choice = _TAppraisalChoice()
a_status_choice = _AStatusChoice()
change_reason_choice = _ChangeChoice()
