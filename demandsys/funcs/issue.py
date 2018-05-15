from demandsys.models import ProductDemand
from base.exceptions import default_exception, Error500, Error404
from usersys.funcs.utils.sid_management import sid_getuser
from demandsys.forms import UploadPhotoForm

from django.http import HttpResponse


def upload_photo(user_sid, dmid, photo_from_object):
    """
    
    :param user_sid: 
    :param dmid:  photo's id
    :return: 
    """
    # check user
    user = sid_getuser(user_sid)
    if user is None:
        raise Error404("user_id do not exist")

    # TODO: set the photo form
    # TODO: check photo size & format
    # TODO: save photo to database

def delete_photo(user_sid, id):
    """
    
    :param user_sid: 
    :param id: 
    :return: 
    """
    # TODO: check whether photo id exists
    # TODO: delete photo


def publish_demand(user_sid, demand, photo_ids):
    """
    
    :param user_sid: 
    :param demand: 
    :param photo_ids: 
    :return: 
    """
    pass

def edit_demand_on_off(user_id, id, demand, photo_ids):
    """
    
    :param user_id: 
    :param id: 
    :param demand: 
    :param photo_ids: 
    :return: 
    """
    pass


def shut_demand(user_sid, id):
    """
    
    :param user_sid: 
    :param id: 
    :return: 
    """
    pass



















