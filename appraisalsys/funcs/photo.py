from django.forms import modelform_factory
from usersys.funcs.utils.usersid import user_from_sid
from usersys.models import UserBase
from usersys.model_choices.user_enum import role_choice
from base.exceptions import WLException, Error404, Error500, default_exception
from simplified_invite.models import InviteInfo
from appraisalsys.models import CheckPhoto


@default_exception(Error500)
@user_from_sid(Error404)
def upload_check_photo(user, ivid, photo_files_from_obj):
    # type: (UserBase, InviteInfo, object) -> int
    if not (user.role == role_choice.BUYER and user == ivid.uid_s):
        raise WLException(403, "no access to upload this photo")

    # submit
    photo = CheckPhoto(in_use=True, uploader=user)
    submit_form = modelform_factory(
        CheckPhoto, fields=('check_photo', )
    )(files=photo_files_from_obj, instance=photo)
    if submit_form.is_valid():
        submit_form.save()
        return photo.id
    else:
        raise WLException(400, str(submit_form.errors))


@default_exception(Error500)
@user_from_sid(Error404)
def delete_check_photo(user, photo_id):
    # type: (UserBase, int) -> None
    try:
        photo = CheckPhoto.objects.get(id=photo_id)
    except CheckPhoto.DoesNotExist:
        raise WLException(404, "no such photo_id")

    if user != photo.uploader:
        raise WLException(403, "no accsee to delete")

    photo.in_use = False
    photo.save()


def get_photo_obj(user, photo_id):
    # type: (UserBase, int) -> CheckPhoto
    try:
        photo = CheckPhoto.objects.get(id=photo_id)
        if photo.uploader != user:
            raise CheckPhoto.DoesNotExist

        return photo
    except CheckPhoto.DoesNotExist:
        raise WLException(404, "no such photo")



@default_exception(Error500)
@user_from_sid(Error404)
def get_check_photo(user, photo_id):
    # type: (UserBase, int) -> str
    photo = get_photo_obj(user, photo_id)
    return photo.check_photo.path
