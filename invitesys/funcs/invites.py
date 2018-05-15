from base.exceptions import WLException, default_exception, Error500, Error404
from base.util.misc_validators import validators
from usersys.models.user_enum import validate_status_choice
from usersys.models import UserBase, UserValidate
from usersys.funcs.utils.usersid import user_from_sid
from invitesys.models.invite_enum import t_invite_choice, i_status_choice, handle_method_choice
from invitesys.models import InviteInfo
from .contracts import create_contract, get_current_template

MAP_TINVITE_INVITE_STATUS = {
    t_invite_choice.PROCEEDING_INVITES_MINE: (
        i_status_choice.STARTED,
        i_status_choice.CONFIRMED,
    ),
    t_invite_choice.CLOSED_INVITES_MINE: (
        i_status_choice.SIGNED,
        i_status_choice.CANCELED,
        i_status_choice.REJECTED,
        i_status_choice.CONTRACT_NOT_AGREE,
    ),
    t_invite_choice.PROCEEDING_INVITES_OTHERS: (
        i_status_choice.STARTED,
        i_status_choice.CONFIRMED,
    ),
    t_invite_choice.CLOSED_INVITES_OTHERS: (
        i_status_choice.SIGNED,
        i_status_choice.REJECTED,
        i_status_choice.CONTRACT_NOT_AGREE,
    )
}


@default_exception(Error500)
@user_from_sid(Error404)
def obtain(user, t_invite, page, count_pre_page):
    """
    :param user:
    :param t_invite:
    :param page: page number
    :return: invites, n_pages
    """
    # FIXME: Order by date
    if t_invite in (t_invite_choice.PROCEEDING_INVITES_MINE, t_invite_choice.CLOSED_INVITES_MINE):
        qs = user.user_invite_src.filter(i_status__in=MAP_TINVITE_INVITE_STATUS[t_invite])
    elif t_invite in (t_invite_choice.PROCEEDING_INVITES_OTHERS, t_invite_choice.CLOSED_INVITES_OTHERS):
        qs = user.user_invite_dst.filter(i_status__in=MAP_TINVITE_INVITE_STATUS[t_invite])
    else:
        raise WLException(400, "t_invite is invalid")
    n_pages = qs.count() + (count_pre_page - 1) / count_pre_page
    if page > n_pages or page < 0:
        raise WLException(400, "Page out of range")

    start = page * count_pre_page
    end = (page + 1) * count_pre_page
    return qs[start: end], n_pages


@default_exception(Error500)
@user_from_sid(Error404)
def detail(user, ivid):
    """

    :param user:
    :param ivid:
    :return: invite, contracts
    """
    try:
        iv = InviteInfo.objects.get(id=ivid)
    except InviteInfo.DoesNotExist:
        raise WLException(404, "No such invite.")

    if iv.uid_s != user and iv.uid_t != user:
        raise WLException(404, "No such invite")

    return iv


@default_exception(Error500)
@user_from_sid(Error404)
def publish(user, invite):
    """

    :param user: user object
    :param invite: invite data
    :return:
    """
    # First check if the user is validated
    try:
        if user.user_validate.validate_status != validate_status_choice.ACCEPTED:
            raise UserBase.DoesNotExist
    except UserValidate.DoesNotExist:
        raise WLException(403, "User's validation does not passed, cannot publish.")

    # Validate whether
    invite["dmid_t"].validate_satisfy_demand(user.role, invite["quantity"])

    invite_obj = InviteInfo(**invite)

    # Auto fill missing fields
    invite_obj.uid_s = user
    invite_obj.uid_t = invite["dmid_t"].uid
    invite_obj.i_status = i_status_choice.STARTED

    # publish invite
    invite_obj.save()
    return invite_obj


@default_exception(Error500)
@user_from_sid(Error404)
def handle(user, ivid, handle_method, reason=None):
    """

    :param user:
    :param ivid:
    :param handle_method:
    :param reason:
    :return:
    """

    def check(u, i, hm, r):
        try:
            i_obj = InviteInfo.objects.get(id=i)
            if u != i_obj.uid_s and u != i_obj.uid_t:
                raise InviteInfo.DoesNotExist

        except InviteInfo.DoesNotExist:
            raise WLException(404, "No such invite.")

        if hm == handle_method_choice.ACCEPT or hm == handle_method_choice.REJECT:
            if u != i_obj.uid_t:
                raise WLException(403, "Inviter cannot accept or reject the invite.")

        if hm == handle_method_choice.CANCEL:
            if u != i_obj.uid_s:
                raise WLException(400, "Invitee cannot cancel the invite, use Reject instead.")

        if hm == handle_method_choice.REJECT or hm == handle_method_choice.CANCEL:
            if not validators.validate(r, "reason"):
                raise WLException(400, "Validation on reason field does not passed.")

        return i_obj

    # Check ivid and the relationship
    iv_obj = check(user, ivid, handle_method, reason)

    # TODO: Log here

    if handle_method == handle_method_choice.ACCEPT:
        iv_obj.i_status = i_status_choice.CONFIRMED
        iv_obj.save()
        create_contract(iv_obj, get_current_template())
        return

    if handle_method == handle_method_choice.REJECT:
        iv_obj.i_status = i_status_choice.REJECTED
        iv_obj.reason = reason
        iv_obj.save()
        return

    if handle_method == handle_method_choice.CANCEL:
        iv_obj.i_status = i_status_choice.CANCELED
        iv_obj.reason = reason
        iv_obj.save()
        return
