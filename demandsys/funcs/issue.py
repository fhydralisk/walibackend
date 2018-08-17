from django.db import transaction

from base.exceptions import default_exception, Error500
from base.util.db import update_instance_from_dict
from demandsys.forms import UploadPhotoForm
from demandsys.models import ProductDemand, ProductDemandPhoto
from demandsys.models.translaters import t_demand_translator
from usersys.funcs.utils.usersid import user_from_sid
from demandsys.funcs.placeholder2exceptions import get_placeholder2exception, change_error_message

@default_exception(Error500)
@user_from_sid(get_placeholder2exception("demand/publish/submit_photo/ : user_sid error"))
def upload_photo(user, photo_from_object, dmid=None):
    """

    :param user:
    :param dmid:
    :param photo_from_object:
    :return:
    """

    if not user.is_validated:
        raise get_placeholder2exception("demand/publish/submit_photo/ : user is not validated")

    # user exits
    photo = ProductDemandPhoto()
    if dmid is not None:
        try:
            demand = ProductDemand.objects.get(id=dmid)
            if demand.uid != user:
                raise get_placeholder2exception("demand/publish/submit_photo/ : no such demand")
        except ProductDemand.DoesNotExist:
            raise get_placeholder2exception("demand/publish/submit_photo/ : no such demand")
        
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
        change_error_message("demand/publish/submit_photo/ : photo error", 403, str(form.errors))
        raise get_placeholder2exception("demand/publish/submit_photo/ : photo error")


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("demand/publish/remove_photo/ : user_sid error"))
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
            raise get_placeholder2exception("demand/publish/remove_photo/ : no access")
    except ProductDemandPhoto.DoesNotExist:
        raise get_placeholder2exception("demand/publish/remove_photo/ : no such photo")

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
@user_from_sid(get_placeholder2exception("demand/publish/publish_demand/ : user_sid error"))
def publish_demand(user, demand, photo_ids=None):
    """
    
    :param user: 
    :param demand: 
    :param photo_ids: 
    :return: 
    """
    if not user.is_validated:
        raise get_placeholder2exception("demand/publish/publish_demand/ : user is not validated")

    if demand["min_quantity"] > demand["quantity"]:
        raise get_placeholder2exception("demand/publish/publish_demand/ : quantity error")

    demand_instance = ProductDemand(**demand)

    # Auto fill some of the fields
    demand_instance.t_demand = t_demand_translator.from_role(user.role)
    demand_instance.pid = demand["qid"].t3id
    demand_instance.uid = user
    demand_instance.save()

    if photo_ids is not None:
        append_photo(demand_instance, photo_ids)

    return demand_instance.id


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("demand/publish/edit_demand/ : user_sid error"))
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
        raise get_placeholder2exception("demand/publish/edit_demand/ : no such demand")

    update_instance_from_dict(instance=demand_object, dic=demand, save=False)

    if demand_object.min_quantity > demand_object.quantity:
        raise get_placeholder2exception("demand/publish/edit_demand/ : quantity error")

    # TODO: check

    with transaction.atomic():
        demand_object.save()
        if photo_ids is not None:
            append_photo(demand_object, photo_ids, True)

    return id


@default_exception(Error500)
@user_from_sid(get_placeholder2exception('demand/publish/close_demand/ : user_sid error'))
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
        raise get_placeholder2exception("demand/publish/close_demand/ : no such demand")


@default_exception(Error500)
@user_from_sid(get_placeholder2exception('demand/publish/remove_demand/ : user_sid error'))
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
        raise get_placeholder2exception('demand/publish/remove_demand/ : no such demand')
