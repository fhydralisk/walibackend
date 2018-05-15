from base.exceptions import *
from demandsys.models import ProductDemand, ProductDemandPhoto
from base.exceptions import default_exception, Error500, Error404
from usersys.funcs.utils.sid_management import sid_getuser
from demandsys.forms import UploadPhotoForm

from usersys.funcs.utils.usersid import user_from_sid

from django.http import HttpResponse


@default_exception(Error500)
@user_from_sid(Error404)
def upload_photo(user, dmid, photo_from_object):
    """
    
    :param user_sid: 
    :param dmid:  photo's id
    :return: 
    """
    # TODO: validate the photo

    photo = ProductDemandPhoto()
    photo.dmid = dmid
    form = UploadPhotoForm(files=photo_from_object, instance=photo)
    #TODO: photo snapshot editing
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
    photo_to_delete = user.demand_photo.filter(inuse=True,id=id)
    if photo_to_delete.is_valid():
        photo_to_delete.inuse = False
        photo_to_delete.save()
    else:
        raise Error404('user_sid not found')


@default_exception(Error500)
@user_from_sid(Error404)
def publish_demand(user, demand, photo_ids):
    """
    
    :param user: 
    :param demand: 
    :param photo_ids: 
    :return: 
    """
    # put demand object into user, don't know how to write
    demand.uid = user

    # TODO: link photo_ids to demand





def edit_demand_on_off(user, id, demand, photo_ids):
    """
    
    :param user_id: 
    :param id: 
    :param demand: 
    :param photo_ids: 
    :return: 
    """
    demand.filter.get(id=id).match = True
    #TODO: edit field_errors



def shut_demand(user, id):
    """
    
    :param user_sid: 
    :param id: 
    :return: 
    """
    demand_object = user.user_demand.objects.get(id=id)
    demand_object.match = False
    demand_object.inuse = False





















