from django.db import transaction

from base.exceptions import default_exception, Error500, Error404, Error403, Error400, WLException
from base.util.db import update_instance_from_dict
from demandsys.forms import UploadPhotoForm
from demandsys.models import ProductDemand, ProductDemandPhoto
from demandsys.models.translaters import t_demand_translator
from usersys.funcs.utils.usersid import user_from_sid


@default_exception(Error500)
@user_from_sid(Error404)
def upload_photo(user, photo_from_object, dmid=None):
    """

    :param user:
    :param dmid:
    :param photo_from_object:
    :return:
    """

    # user exits
    photo = ProductDemandPhoto()
    if dmid is not None:
        try:
            demand = ProductDemand.objects.get(id=dmid)
            if demand.uid != user:
                raise Error404("No such demand")
        except ProductDemand.DoesNotExist:
            raise Error404("No such demand")
        
        photo.dmid = demand
        photo.inuse = True
    else:
        photo.inuse = False
    
    form = UploadPhotoForm(files=photo_from_object, instance=photo)
    # TODO: photo snapshot editing
    if form.is_valid():
        form.save()
        return photo.id
    else:
        raise Error403(str(form.errors))


@default_exception(Error500)
@user_from_sid(Error404)
def delete_photo(user, id):
    """
    
    :param user_sid: 
    :param id: 
    :return: 
    """
    #  check whether photo id exists
    try:
        photo_to_delete = ProductDemandPhoto.objects.get(id=id, inuse=True)
        if photo_to_delete.dmid.uid != user:
            raise ProductDemandPhoto.DoesNotExist
    except ProductDemandPhoto.DoesNotExist:
        raise Error404("No such photo")

    photo_to_delete.dmid = None
    photo_to_delete.inuse = False
    photo_to_delete.save()


def append_photo(demand_object, photo_ids, do_cleanup=False):
    photos = ProductDemandPhoto.objects.filter(id__in=photo_ids, inuse=False, dmid=None)
    photos.update(dmid=demand_object, inuse=True)

    if do_cleanup:
        # remove photos not in the list
        photos_remove = ProductDemandPhoto.objects.filter(inuse=True, dmid=demand_object).exclude(id__in=photo_ids)
        photos_remove.update(inuse=False, dmid=None)


@default_exception(Error500)
@user_from_sid(Error404)
def publish_demand(user, demand, photo_ids=None):
    """
    
    :param user: 
    :param demand: 
    :param photo_ids: 
    :return: 
    """
    if not user.is_validated:
        raise WLException(410, "User's validation does not passed, cannot publish.")

    if demand["min_quantity"] > demand["quantity"]:
        raise Error400("min_quantity must equal to or less than quantity")

    demand_instance = ProductDemand(**demand)

    # Auto fill some of the fields
    demand_instance.t_demand = t_demand_translator.from_role(user.role)
    demand_instance.uid = user
    demand_instance.save()

    if photo_ids is not None:
        append_photo(demand_instance, photo_ids)

    return demand_instance.id


@default_exception(Error500)
@user_from_sid(Error404)
def edit_demand(user, id, demand, photo_ids=None):
    """
    
    :param user:
    :param id: 
    :param demand: 
    :param photo_ids: 
    :return: 
    """
    try:
        demand_object = ProductDemand.objects.get(id=id, uid=user, in_use=True)
    except ProductDemand.DoesNotExist:
        raise Error404("No such demand")

    update_instance_from_dict(instance=demand_object, dic=demand, save=False)

    if demand_object.min_quantity > demand_object.quantity:
        raise Error400("min_quantity must equal to or less than quantity")

    # TODO: check

    with transaction.atomic():
        demand_object.save()
        if photo_ids is not None:
            append_photo(demand_object, photo_ids, True)

    return id


@default_exception(Error500)
@user_from_sid(Error404)
def shut_demand(user, id):
    """

    :param user:
    :param id:
    :return:
    """

    try:
        demand_object = ProductDemand.objects.get(id=id, uid=user, in_use=True)
        demand_object.match = False
        demand_object.save()
    except ProductDemand.DoesNotExist:
        raise Error404("No such demand")


@default_exception(Error500)
@user_from_sid(Error404)
def delete_demand(user, id):
    """

    :param user:
    :param id:
    :return:
    """

    try:
        demand_object = ProductDemand.objects.get(id=id, uid=user, in_use=True)
        demand_object.match = False
        demand_object.in_use = False
        demand_object.save()
    except ProductDemand.DoesNotExist:
        raise Error404("No such demand")

