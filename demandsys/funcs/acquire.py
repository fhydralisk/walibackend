from demandsys.models import ProductDemand, ProductDemandPhoto
from base.exceptions import default_exception, Error500, Error404, Error400
from base.util.timestamp import now
from base.util.pages import get_page_info, get_page_info_list
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
    ).filter(
        in_use=True, closed=False, end_time__gt=now()
    ).exclude(t_demand=t_demand_translator.from_role(role)).order_by("-id")

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
    ).filter(uid=user, in_use=True).order_by("-id")

    st, ed, n_pages = get_page_info(qs, count_per_page, page, index_error_excepiton=Error400("Page out of range"))
    # return sliced single page
    return qs[st:ed], n_pages


@default_exception(Error500)
@user_from_sid(Error404)
def get_matched_demand(user, id, page, count_per_page):
    """
    :param user:
    :param id:
    :param page:
    :return:
    """

    def confirm_satisfied(self, other):
        # type: (ProductDemand, ProductDemand) -> bool
        return self.quantity_metric() > other.min_quantity_metric()

    def match_key(m):
        return demand.match_score(m)["score_overall"]

    try:
        demand = ProductDemand.objects.select_related(
            'uid__user_validate',
            'qid__t3id__t2id__t1id',
            'aid__cid__pid',
            'pmid', 'wcid'
        ).get(in_use=True, id=id, uid=user)
    except ProductDemand.DoesNotExist:
        raise Error404("No such demand.")

    match_queryset = ProductDemand.objects.select_related(
        'uid__user_validate',
        'qid__t3id__t2id__t1id',
        'aid__cid__pid',
        'pmid', 'wcid'
    ).filter(
        in_use=True,            # Must be in use
        closed=False,
        match=True,
        qid=demand.qid,
        aid__cid__pid=demand.aid.cid.pid
    ).exclude(
        uid__role=user.role     # Exclude same role
    ).filter(
        end_time__gt=now(),
    )

    # FIXME: Here we got a efficient issue, Every time user use this api, it will query the full set
    # of matched queryset. We must figure out how to fetch it by page, or ... cache it.
    maches = match_queryset.all()
    matches_list = [
        m for m in maches if confirm_satisfied(demand, m)
    ]
    matches_list.sort(key=match_key, reverse=True)

    st, ed, n_pages = get_page_info_list(
        matches_list, count_per_page, page, index_error_excepiton=Error400("Page out of range")
    )

    # return sliced single page
    return demand, matches_list[st:ed], n_pages


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
def get_specified_photo(id):
    """
    
    :param id: 
    :param dmid: 
    :return: 
    """
    try:
        return ProductDemandPhoto.objects.get(id=id).demand_photo.path
    except ProductDemandPhoto.DoesNotExist:
        raise Error404("No such photo.")

