from django.forms import modelform_factory
from base.exceptions import default_exception, Error500
from usersys.funcs.utils.usersid import user_from_sid
from usersys.models import UserBase
from usersys.model_choices.user_enum import role_choice
from ordersys.models import OrderReceiptPhoto, OrderInfo
from ordersys.model_choices.order_enum import o_status_choice
from ordersys.model_choices.photo_enum import photo_type_choice
from base.util.placeholder2exceptions import get_placeholder2exception

def check_role(user, photo_type):
    # type: (UserBase, int) -> bool
    if (
            user.role == role_choice.BUYER and photo_type == photo_type_choice.RECEIPT_CHECK
    ) or (
            user.role == role_choice.SELLER and photo_type in (photo_type_choice.RECEIPT_FORWARD, photo_type_choice.PHOTO_PRODUCTS)
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
        raise get_placeholder2exception("order/photo/obtain/ : no such photo")


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("order/photo/upload/ : user_sid error"))
def upload_order_photo(user, oid, t_photo, photo_files_form_obj):
    # type: (UserBase, OrderInfo, int, object) -> int
    invite = oid.ivid
    if invite.uid_s != user and invite.uid_t != user:
        raise get_placeholder2exception("order/photo/upload/ : no such oid")

    # Check photo type and user role permissions
    if not check_photo_type(oid.o_status, t_photo):
        raise get_placeholder2exception("order/photo/upload/ : cannot submit this photo")

    if not check_role(user, t_photo):
        raise get_placeholder2exception("order/photo/upload/ : user role does not match")

    # Real submit
    photo = OrderReceiptPhoto(photo_type=t_photo, oid=oid, in_use=True)
    submit_form = modelform_factory(
        OrderReceiptPhoto, fields=('receipt_photo', )
    )(files=photo_files_form_obj, instance=photo)
    if submit_form.is_valid():
        submit_form.save()
        return photo.id
    else:
        raise get_placeholder2exception("order/photo/uoload/ : photo error", error_message=str(submit_form.errors))


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("order/photo/delete/ : user_sid error"))
def delete_order_photo(user, photo_id):
    # type: (UserBase, int) -> None
    photo = get_photo_obj(user, photo_id)
    
    photo_type = photo.photo_type

    if not check_photo_type(photo.oid.o_status, photo_type):
        raise get_placeholder2exception("order/photo/delete/ : cannot remove")

    if not check_role(user, photo_type):
        raise get_placeholder2exception("order/photo/delete/ : user role error")

    photo.in_use = False
    photo.save()
    

@default_exception(Error500)
@user_from_sid(get_placeholder2exception("order/photo/obtain/ : user_sid_error"))
def get_order_photo(user, photo_id):
    # type: (UserBase, int) -> str
    photo = get_photo_obj(user, photo_id)
    return photo.receipt_photo.path
