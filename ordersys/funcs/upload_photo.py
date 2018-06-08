from django.forms import modelform_factory
from base.exceptions import default_exception, Error404, Error500, WLException
from usersys.funcs.utils.usersid import user_from_sid
from usersys.models import UserBase
from usersys.model_choices.user_enum import role_choice
from ordersys.models import OrderReceiptPhoto, OrderInfo
from ordersys.model_choices.order_enum import o_status_choice
from ordersys.model_choices.photo_enum import photo_type_choice


def check_role(user, photo_type):
    # type: (UserBase, int) -> bool
    if (
            user.role == role_choice.BUYER and photo_type == photo_type_choice.RECEIPT_CHECK
    ) or (
            user.role == role_choice.SELLER and photo_type == photo_type_choice.RECEIPT_FORWARD
    ):
        return True
    else:
        return False


def check_photo_type(o_status, t_photo):
    if o_status == o_status_choice.WAIT_PRODUCT_CHECK:
        if t_photo == photo_type_choice.RECEIPT_CHECK:
            return True

    elif o_status == o_status_choice.WAIT_PRODUCT_DELIVER:
        if t_photo in (photo_type_choice.RECEIPT_FORWARD, photo_type_choice.PHOTO_PRODUCTS):
            return True

    return False


def get_photo_obj(user, photo_id):
    # type: (UserBase, int) -> OrderReceiptPhoto
    try:
        photo = OrderReceiptPhoto.objects.select_related('oid__ivid').get(id=photo_id, in_use=True)
        invite = photo.oid.ivid
        if invite.uid_s != user and invite.uid_t != user:
            raise OrderReceiptPhoto.DoesNotExist

        return photo
    except OrderReceiptPhoto.DoesNotExist:
        raise WLException(404, "No such photo")


@default_exception(Error500)
@user_from_sid(Error404)
def upload_order_photo(user, order, t_photo, photo_files_form_obj):
    # type: (UserBase, OrderInfo, int, object) -> int
    invite = order.ivid
    if invite.uid_s != user and invite.uid_t != user:
        raise WLException(404, "No such order")

    # Check photo type and user role permissions
    if not check_photo_type(order.o_status, t_photo):
        raise WLException(403, "Cannot submit this photo")

    if not check_role(user, t_photo):
        raise WLException(403, "User role does not match the photo submit action.")

    # Real submit
    photo = OrderReceiptPhoto(photo_type=t_photo, oid=order, in_use=True)
    submit_form = modelform_factory(
        OrderReceiptPhoto, fields=('receipt_photo', )
    )(files=photo_files_form_obj, instance=photo)
    if submit_form.is_valid():
        submit_form.save()
        return photo.id
    else:
        raise WLException(400, str(submit_form.errors))


@default_exception(Error500)
@user_from_sid(Error404)
def delete_order_photo(user, photo_id):
    # type: (UserBase, int) -> None
    photo = get_photo_obj(user, photo_id)
    
    photo_type = photo.photo_type

    if not check_photo_type(photo.oid.o_status, photo_type):
        raise WLException(403, "Cannot remove this photo")

    if not check_role(user, photo_type):
        raise WLException(403, "User role does not match the photo delete action.")

    photo.in_use = False
    photo.save()
    

@default_exception(Error500)
@user_from_sid(Error404)
def get_order_photo(user, photo_id):
    # type: (UserBase, int) -> str
    photo = get_photo_obj(user, photo_id)
    return photo.receipt_photo.path
