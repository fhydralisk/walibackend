from demandsys.models import ProductDemand
from base.exceptions import default_exception, Error500, Error404, Error400
from base.util.pages import get_page_info
from usersys.funcs.utils.usersid import user_from_sid
from demandsys.models.translaters import t_demand_translator


@default_exception(Error500)
@user_from_sid(None)
def get_popular_demand(role, user, page, count_per_page):
    """
    :param role: 
    :param user:
    :param page: start from one
    :param count_per_page: size of page
    :return: 
    """

    if user is None and role is None:
        raise Error400("Either user or role must not be null.")

    if user is not None:
        role = user.role

    qs = ProductDemand.objects.select_related(
        'uid__user_validate',
        'qid__t3id__t2id__t1id',
        'aid__cid__pid',
        'pmid', 'wcid'
    ).filter(in_use=True).exclude(t_demand=t_demand_translator.from_role(role))

    st, ed, n_pages = get_page_info(qs, count_per_page, page, index_error_excepiton=Error400("Page out of range"))

    # return sliced single page
    return qs[st:ed], n_pages


@default_exception(Error500)
@user_from_sid(Error404)
def get_my_demand(user, page, count_per_page):
    """
    TODO: using user_sid to get specified page
    :param user:
    :param page:
    :param count_per_page
    :return: 
    """

    qs = ProductDemand.objects.select_related(
        'uid__user_validate',
        'qid__t3id__t2id__t1id',
        'aid__cid__pid',
        'pmid', 'wcid'
    ).filter(uid=user, in_use=True)

    st, ed, n_pages = get_page_info(qs, count_per_page, page, index_error_excepiton=Error400("Page out of range"))
    # return sliced single page
    return qs[st:ed], n_pages


# TODO: Figure this out later

# @default_exception(Error500)
# @user_from_sid(Error404)
# def get_matched_demand(user, id, page):
#     """
#     TODO: DemandMatchingScore not set
#     :param user_sid:
#     :param id:
#     :param page:
#     :return:
#     """
#     # page_size = 3  # number of items per page
#     page = int(page)
#
#     # TODO: match the specific id
#     demand = ProductDemand.objects.filter(id=id)
#
#     # return sliced single page
#     if page < 1:
#         raise Error404('Page number must be positive int')
#     else:
#         return ProductDemand.objects.filter(in_use=True)[(page - 1) * page_size: page * page_size]


@default_exception(Error500)
@user_from_sid(None)
def get_demand_detail(user, id):
    """

    :param user:
    :param id:
    :return:
    """

    try:
        demand = ProductDemand.objects.select_related(
            'uid__user_validate',
            'qid__t3id__t2id__t1id',
            'aid__cid__pid',
            'pmid', 'wcid'
        ).get(in_use=True, id=id)
    except ProductDemand.DoesNotExist:
        raise Error404("No such demand.")
    return demand


@default_exception(Error500)
@user_from_sid(Error404)
def get_specified_photo(id, dmid):
    """
    
    :param id: 
    :param dmid: 
    :return: 
    """
    return ProductDemand.objects.select_related(
        'uid__user_validate',
        'qid__t3id__t2id__t1id',
        'aid__cid__pid',
        'pmid', 'wcid'
    ).filter(in_use=True, id=dmid)

