from django.db.models.signals import post_save
from django.dispatch import receiver
from simplified_invite.models import InviteInfo
from appraisalsys.models import AppraisalInfo
from logsys.models import LogInviteStatus
from base.exceptions import WLException, default_exception, Error500, Error404
from usersys.funcs.utils.usersid import user_from_sid
from usersys.models import UserBase


@receiver(post_save, sender=InviteInfo)
def log_invite_change(instance, **kwargs):
    # type: (InviteInfo, dict) -> None
    operator = None
    log_entry = LogInviteStatus(ivid=instance, operator=operator, i_status=instance.i_status)
    log_entry.save()


@default_exception(Error500)
@user_from_sid(Error404)
def obtain_invite_and_appraisal_log(user, ivid):
    # type: (UserBase, InviteInfo) -> (QuerySet, AppraisalInfo)
    invite = ivid
    if invite.uid_s != user and invite.uid_t != user:
        raise WLException(404, "No such invite")

    try:
        ret = (LogInviteStatus.objects.filter(ivid=ivid).order_by('id'), ivid.appraisal.history.last())
    except AppraisalInfo.DoesNotExist:
        ret = (LogInviteStatus.objects.filter(ivid=ivid).order_by('id'), None)

    return ret


@default_exception(Error500)
@user_from_sid(Error404)
def check_invite_user(user, ivid):
    invite = ivid
    if invite.uid_s != user and invite.uid_t != user:
        raise WLException(404, "No such invite")

    return invite, user
