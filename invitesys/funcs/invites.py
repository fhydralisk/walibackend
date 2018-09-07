from django.forms import modelform_factory
from base.exceptions import WLException, default_exception, Error500, Error404
from base.util.misc_validators import validators
from base.util.pages import get_page_info
from usersys.funcs.utils.usersid import user_from_sid
from usersys.model_choices.user_enum import role_choice
from usersys.models import UserBase
from demandsys.util.unit_converter import UnitQuantityMetric
from invitesys.model_choices.invite_enum import t_invite_choice, i_status_choice, handle_method_choice
from invitesys.models import InviteInfo, InviteCancelReason, InviteProductPhoto
from .contracts import create_contract, get_current_template

MAP_TINVITE_INVITE_STATUS = {
    t_invite_choice.PROCEEDING_INVITES: (
        i_status_choice.STARTED,
        i_status_choice.INVITER_NEGOTIATE,
        i_status_choice.INVITEE_NEGOTIATE,
        i_status_choice.CONFIRMED,
    ),
    t_invite_choice.CLOSED_INVITES: (
        i_status_choice.CANCELED,
        i_status_choice.REJECTED,
        i_status_choice.CONTRACT_NOT_AGREE,
    ),
    t_invite_choice.FINISHED_INVITES: (
        i_status_choice.SIGNED,
    )
}


@default_exception(Error500)
@user_from_sid(Error404)
def obtain(user, t_invite, page, count_pre_page):
    """
    :param user:
    :param t_invite:
    :param page: page number
    :param count_pre_page
    :return: invites, n_pages
    """

    # if t_invite in (
    #     t_invite_choice.PROCEEDING_INVITES_MINE,
    #     t_invite_choice.CLOSED_INVITES_MINE,
    #     t_invite_choice.FINISHED_INVITES_MINE,
    # ):
    #     qs = user.user_invite_src.select_related(
    #         'dmid_t__qid__t3id__t2id__t1id',
    #         'dmid_t__wcid',
    #         'uid_s__user_validate',
    #         'uid_t__user_validate'
    #     ).filter(i_status__in=MAP_TINVITE_INVITE_STATUS[t_invite])
    # elif t_invite in (
    #     t_invite_choice.PROCEEDING_INVITES_OTHERS,
    #     t_invite_choice.CLOSED_INVITES_OTHERS,
    #     t_invite_choice.FINISHED_INVITES_OTHERS,
    # ):
    #     qs = user.user_invite_dst.select_related(
    #         'dmid_t__qid__t3id__t2id__t1id',
    #         'dmid_t__wcid',
    #         'uid_s__user_validate',
    #         'uid_t__user_validate'
    #     ).filter(i_status__in=MAP_TINVITE_INVITE_STATUS[t_invite])
    # else:
    #     raise WLException(400, "t_invite is invalid")

    qs1 = user.user_invite_src.select_related(
        'dmid_t__qid__t3id__t2id__t1id',
        'dmid_t__wcid',
        'uid_s__user_validate',
        'uid_t__user_validate'
    ).filter(i_status__in=MAP_TINVITE_INVITE_STATUS[t_invite])

    qs2 = user.user_invite_dst.select_related(
        'dmid_t__qid__t3id__t2id__t1id',
        'dmid_t__wcid',
        'uid_s__user_validate',
        'uid_t__user_validate'
    ).filter(i_status__in=MAP_TINVITE_INVITE_STATUS[t_invite])

    qs = qs1 | qs2

    start, end, n_pages = get_page_info(
        qs, count_pre_page, page, index_error_excepiton=WLException(400, "Page out of range")
    )

    qs = qs.order_by('-id')
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
        iv = InviteInfo.objects.select_related(
            'dmid_t__qid__t3id__t2id__t1id',
            'dmid_t__wcid',
            'uid_s__user_validate',
            'uid_t__user_validate'
        ).get(id=ivid)
    except InviteInfo.DoesNotExist:
        raise WLException(404, "No such invite.")

    if iv.uid_s != user and iv.uid_t != user:
        raise WLException(404, "No such invite")

    return iv


@default_exception(Error500)
@user_from_sid(Error404)
def publish(user, invite, invite_photos=None):
    """

    :param user: user object
    :param invite: invite data
    :param invite_photos
    :return:
    """
    # First check if the user is validated
    if not user.is_validated:
        raise WLException(410, "User's validation does not passed, cannot publish.")

    # Validate whether
    invite["dmid_t"].validate_satisfy_demand(
        user.role, quantity=invite['quantity']
    )

    invite_obj = InviteInfo(**invite)

    # Auto fill missing fields

    if user.role == role_choice.SELLER:
        invite_obj.aid = invite["dmid_t"].aid
        invite_obj.street = invite["dmid_t"].street
        invite_obj.abid = invite["dmid_t"].abid

    invite_obj.uid_s = user
    invite_obj.uid_t = invite["dmid_t"].uid
    invite_obj.i_status = i_status_choice.STARTED

    # publish invite
    invite_obj.save()

    # create invite photos
    if invite_obj.seller_demand is not None:
        dm_photos = invite_obj.seller_demand.demand_photo.filter(inuse=True)
        for dm_photo in dm_photos:
            InviteProductPhoto.objects.create(
                ivid=invite_obj,
                uploader=user,
                invite_photo=dm_photo.demand_photo,
                invite_photo_snapshot=dm_photo.demand_photo_snapshot,
                inuse=True,
                photo_desc=dm_photo.photo_desc
            )

    if user.role == role_choice.SELLER:

        # bind invite photo
        exc = WLException(400, "invite_photos contains invalid photo id.")
        if invite_photos is not None:
            photo_objs = InviteProductPhoto.objects.select_related('ivid').filter(id__in=invite_photos, inuse=True)
            if photo_objs.count() != len(invite_photos):
                raise exc

            # validate photo first
            for photo_obj in photo_objs:
                if photo_obj.ivid is not None:
                    raise exc
                if photo_obj.uploader != user:
                    raise exc

            # do real update
            photo_objs.update(ivid=invite_obj)

    return invite_obj


@default_exception(Error500)
@user_from_sid(Error404)
def handle(user, ivid, handle_method, price=None, pmid=None, reason=None, reason_class=None):
    """

    :param user:
    :param ivid:
    :param handle_method:
    :param price:
    :param pmid:
    :param reason:
    :param reason_class
    :return: invite object
    """

    def _real_handle():
        if iv_obj.i_status == i_status_choice.STARTED:
            if user == iv_obj.uid_t:
                if handle_method == handle_method_choice.NEGOTIATE:
                    iv_obj.i_status = i_status_choice.INVITEE_NEGOTIATE
                    if price is not None:
                        iv_obj.price = price
                    if pmid is not None:
                        iv_obj.pmid = pmid
                    return

                if handle_method == handle_method_choice.ACCEPT:
                    iv_obj.i_status = i_status_choice.CONFIRMED
                    create_contract(iv_obj, get_current_template())
                    return

                if handle_method == handle_method_choice.REJECT:
                    iv_obj.i_status = i_status_choice.REJECTED
                    iv_obj.reason_class = reason_class
                    iv_obj.reason = reason
                    return

            elif user == iv_obj.uid_s:
                if handle_method == handle_method_choice.CANCEL:
                    iv_obj.i_status = i_status_choice.CANCELED
                    iv_obj.reason_class = reason_class
                    iv_obj.reason = reason
                    return
            else:
                raise AssertionError("user is neither inviter nor invitee.")

        elif iv_obj.i_status in (i_status_choice.INVITEE_NEGOTIATE, i_status_choice.INVITER_NEGOTIATE):
            if handle_method == handle_method_choice.NEGOTIATE:
                if price is not None:
                    iv_obj.price = price
                if pmid is not None:
                    iv_obj.pmid = pmid
                if user == iv_obj.uid_t:
                    iv_obj.i_status = i_status_choice.INVITEE_NEGOTIATE
                elif user == iv_obj.uid_s:
                    iv_obj.i_status = i_status_choice.INVITER_NEGOTIATE
                else:
                    raise AssertionError("user is neither inviter nor invitee.")
                return

            if handle_method == handle_method_choice.ACCEPT:
                if (
                    user == iv_obj.uid_s and iv_obj.i_status == i_status_choice.INVITEE_NEGOTIATE
                    or
                    user == iv_obj.uid_t and iv_obj.i_status == i_status_choice.INVITER_NEGOTIATE
                ):
                    iv_obj.i_status = i_status_choice.CONFIRMED
                    create_contract(iv_obj, get_current_template())
                    return

            if handle_method == handle_method_choice.REJECT:
                if (
                    user == iv_obj.uid_s and iv_obj.i_status == i_status_choice.INVITEE_NEGOTIATE
                    or
                    user == iv_obj.uid_t and iv_obj.i_status == i_status_choice.INVITER_NEGOTIATE
                ):
                    iv_obj.i_status = i_status_choice.REJECTED
                    iv_obj.reason_class = reason_class
                    iv_obj.reason = reason
                    return

            if handle_method == handle_method_choice.CANCEL:
                if (
                        user == iv_obj.uid_t and iv_obj.i_status == i_status_choice.INVITEE_NEGOTIATE
                        or
                        user == iv_obj.uid_s and iv_obj.i_status == i_status_choice.INVITER_NEGOTIATE
                ):
                    iv_obj.i_status = i_status_choice.CANCELED
                    iv_obj.reason_class = reason_class
                    iv_obj.reason = reason
                    return

        elif iv_obj.i_status == i_status_choice.CONFIRMED:
            pass
        elif iv_obj.i_status in {
            i_status_choice.CANCELED,
            i_status_choice.REJECTED,
            i_status_choice.SIGNED,
            i_status_choice.CONTRACT_NOT_AGREE
        }:
            pass

        raise WLException(403, "Action Error")

    # TODO: Log here
    try:
        iv_obj = InviteInfo.objects.get(id=ivid)
        if user != iv_obj.uid_s and user != iv_obj.uid_t:
            raise InviteInfo.DoesNotExist

    except InviteInfo.DoesNotExist:
        raise WLException(404, "No such invite.")

    _real_handle()
    iv_obj.save()
    return iv_obj


@default_exception(Error500)
def get_reason_classes():
    return InviteCancelReason.objects.filter(in_use=True).all()


@default_exception(Error500)
@user_from_sid(Error404)
def upload_invite_photo(user, photo_desc, photo_files_form_obj, ivid=None):
    # type: (UserBase, str, object, InviteInfo) -> int
    if ivid is not None:
        if ivid.seller != user:
            raise WLException(404, "No such invite.")

    if user.role != role_choice.SELLER:
        raise WLException(403, "Only seller can submit invite photos.")

    # Real submit
    photo = InviteProductPhoto(ivid=ivid, photo_desc=photo_desc, inuse=True, uploader=user)
    submit_form = modelform_factory(
        InviteProductPhoto, fields=('invite_photo', )
    )(files=photo_files_form_obj, instance=photo)
    if submit_form.is_valid():
        submit_form.save()
        return photo.id
    else:
        raise WLException(400, str(submit_form.errors))


@default_exception(Error500)
@user_from_sid(Error404)
def delete_invite_photo(user, photo_id):
    try:
        photo = InviteProductPhoto.objects.filter(id=photo_id, inuse=True).get()
    except InviteProductPhoto.DoesNotExist:
        raise WLException(404, "No such photo.")

    if photo.uploader != user:
        raise WLException(404, "No such photo.")

    if photo.ivid is not None:
        if photo.ivid.seller != user:
            raise WLException(404, "No such photo.")

        if photo.ivid.i_status not in {
            i_status_choice.STARTED,
        }:
            raise WLException(403, "Cannot delete photo with status %d" % photo.ivid.i_status)

    photo.inuse = False
    photo.save()


@default_exception(Error500)
@user_from_sid(Error404)
def get_invite_photo(user, photo_id):
    # type: (UserBase, int) -> str
    try:
        photo = InviteProductPhoto.objects.filter(id=photo_id, inuse=True).get()
    except InviteProductPhoto.DoesNotExist:
        raise WLException(404, "No such photo.")

    if photo.ivid is not None:
        if photo.ivid.uid_s != user and photo.ivid.uid_t != user:
            raise WLException(404, "No such photo.")
    else:
        if photo.uploader != user:
            raise WLException(404, "No such photo.")

    return photo.invite_photo.path
