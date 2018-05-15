from demandsys.models import ProductDemand
from base.exceptions import default_exception, Error500, Error404
from usersys.funcs.utils.sid_management import sid_getuser

from usersys.funcs.utils.usersid import user_from_sid

page_size = 3


@default_exception(Error500)
@user_from_sid(Error404)
def get_popular_demand(page, **kw):
    """
    #TODO: choose one from role and user_sid
    :param role: 
    :param user_sid: 
    :param page: start from one
    :return: 
    """
    if 'role' in kw.keys():
        number_objects = ProductDemand.objects.filter(in_use=True).user_demand.objects.filter(in_use=True,
                                                                                              role=kw['role'])
    elif 'user_sid' in kw.keys():
        user_role = ProductDemand.objects.filter(uid=kw['user_sid']).user_demand.objects.filter(in_use=True).role
        number_objects = ProductDemand.objects.filter(in_use=True).user_demand.objects.filter(in_use=True,
                                                                                              role=user_role)

    # return sliced single page
    if page < 1 or page > number_objects.count():
        raise Error404('Page number exceeds range')
    else:
        startPage = page * page_size
        endPage = (page + 1) * page_size
        return ProductDemand.objects.filter(in_use=True)[startPage: endPage]

@default_exception(Error500)
def get_my_demand(user_sid, page):
    """
    TODO: using user_sid to get specified page
    :param user_sid: 
    :param page: 
    :return: 
    """
    # check user
    user = sid_getuser(user_sid)
    if user is None:
        raise Error404("user_id do not exist")
    # page_size = 3  # number of items per page
    page = int(page)

    # return sliced single page
    if page < 1:
        raise Error404('Page number must be positive int')
    else:
        return ProductDemand.objects.filter(in_use=True)[(page - 1) * page_size: page * page_size]

@default_exception(Error500)
def get_matched_demand(user_sid, id, page):
    """
    TODO: DemandMatchingScore not set 
    :param user_sid: 
    :param id:
    :param page: 
    :return: 
    """
    # check user
    user = sid_getuser(user_sid)
    if user is None:
        raise Error404("user_id do not exist")
    # page_size = 3  # number of items per page
    page = int(page)

    # TODO: match the specific id
    demand = ProductDemand.objects.filter(id=id)

    # return sliced single page
    if page < 1:
        raise Error404('Page number must be positive int')
    else:
        return ProductDemand.objects.filter(in_use=True)[(page - 1) * page_size: page * page_size]


@default_exception(Error500)
def get_customed_demand(user_sid, id):
    """
    
    :param user_sid: 
    :param id: 
    :param page: 
    :return: 
    """
    # check user
    user = sid_getuser(user_sid)
    if user is None:
        raise Error404("user_id do not exist")

    # TODO: set the page parameter

    customed_demand = ProductDemand.objects.filter(in_use=True, id=id)
    return customed_demand, customed_demand.demand_photo.object.filter(in_use=True)


@default_exception(Error500)
def get_specified_photo(id, dmid):
    """
    
    :param id: 
    :param dmid: 
    :return: 
    """
    return ProductDemand.objects.filter(in_use=True, id=dmid).demand_photo(in_use=True, id=id)

