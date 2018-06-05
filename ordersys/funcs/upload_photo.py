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
def upload_order_photo(user, order, photo_files_form_obj):
    # type: (UserBase, OrderInfo, object) -> int
    invite = order.ivid
    if invite.uid_s != user and invite.uid_t != user:
        raise WLException(404, "No such order")

    if order.o_status not in (o_status_choice.WAIT_PRODUCT_CHECK, o_status_choice.WAIT_PRODUCT_DELIVER):
        raise WLException(403, "Cannot submit photo at this time.")

    photo_type = (
        photo_type_choice.RECEIPT_FORWARD
        if order.o_status == o_status_choice.WAIT_PRODUCT_DELIVER
        else photo_type_choice.RECEIPT_CHECK
    )
    
    # Check user role permissions
    if check_role(user, photo_type):
        photo = OrderReceiptPhoto(photo_type=photo_type, oid=order, in_use=True)
        submit_form = modelform_factory(
            OrderReceiptPhoto, fields=('receipt_photo', )
        )(files=photo_files_form_obj, instance=photo)
        if submit_form.is_valid():
            submit_form.save()
            return photo.id
        else:
            raise WLException(400, str(submit_form.errors))
    
    else:
        raise WLException(403, "User role does not match the photo submit action.")


@default_exception(Error500)
@user_from_sid(Error404)
def delete_order_photo(user, photo_id):
    # type: (UserBase, int) -> None
    photo = get_photo_obj(user, photo_id)
    
    photo_type = photo.photo_type
    if check_role(user, photo_type):
        photo.in_use = False
        photo.save()
    else:
        raise WLException(403, "User role does not match the photo delete action.")
    

@default_exception(Error500)
@user_from_sid(Error404)
def get_order_photo(user, photo_id):
    # type: (UserBase, int) -> str
    photo = get_photo_obj(user, photo_id)
    return photo.receipt_photo.path
