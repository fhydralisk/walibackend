from appraisalsys.models.appraise import AppraisalInfo
from base.exceptions import default_exception, WLException, Error500, Error404
from usersys.funcs.utils.usersid import user_from_sid
from usersys.models import UserBase
from simplified_invite.models import InviteInfo


@default_exception(Error500)
@user_from_sid(Error404)
def obtain_appraisal_log(user, ivid):
    # type: (UserBase, InviteInfo) -> QuerySet

    # Only the buyer can obtain this log.
    if ivid.buyer != user:
        raise WLException(403, "Permission denied.")

    try:
        apprid = ivid.appraisal
        return apprid.history.last()
    except AppraisalInfo.DoesNotExist:
        return None
