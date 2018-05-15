from demandsys.models import ProductDemand
from base.exceptions import default_exception, Error500, Error404
from usersys.funcs.utils.sid_management import sid_getuser

page_size = 3

@default_exception(Error500)
def get_popular_demand(role, user_sid, page):
    """
    #TODO: choose one from role and user_sid
    :param role: 
    :param user_sid: 
    :param page: start from one
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
        return ProductDemand.object.filter(in_use=True)[(page-1) * page_size: page*page_size]

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
        return ProductDemand.object.filter(in_use=True)[(page - 1) * page_size: page * page_size]

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
    demand = ProductDemand.object.filter(id=id)

    # return sliced single page
    if page < 1:
        raise Error404('Page number must be positive int')
    else:
        return ProductDemand.object.filter(in_use=True)[(page - 1) * page_size: page * page_size]


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

    customed_demand = ProductDemand.object.filter(in_use=True, id=id)
    return customed_demand, customed_demand.demand_photo.object.filter(in_use=True)


@default_exception(Error500)
def get_specified_photo(id, dmid):
    """
    
    :param id: 
    :param dmid: 
    :return: 
    """
    return ProductDemand.object.filter(in_use=True, id=dmid).demand_photo(in_use=True, id=id)

