from demandsys.models import ProductDemand, ProductDemandPhoto
from demandsys.model_choices.demand_enum import match_order_choice
from base.exceptions import default_exception, Error500, Error404, Error400
from base.util.timestamp import now
from base.util.pages import get_page_info, get_page_info_list
from usersys.funcs.utils.usersid import user_from_sid
from demandsys.models.translaters import t_demand_translator
from django.db.models import Q, F, Sum


def hide_satisfied(qs):
    # FIXME: only sum simplified_demand_invite_dst
    # Exclude all demands that are already satisfied.
    qs = qs.annotate(
        satisfied_dst=Sum('simplified_demand_invite_dst__appraisal__ivid__quantity')
    ).exclude(~Q(satisfied_dst=None), quantity__lte=(F('satisfied_dst')))
    return qs


def filter_and_order_demand(qs, t1id, aid, asc_of_price):

    if t1id is not None:
        qs = qs.filter(pid__t2id__t1id=t1id)
    if aid is not None:
        qs = qs.filter(aid=aid)
    if asc_of_price is not None:
        if asc_of_price:
            qs = qs.order_by("price", "-id")
        else:
            qs = qs.order_by("-price", "-id")
    else:
        qs = qs.order_by("-id")

    return qs


@default_exception(Error500)
@user_from_sid(None)
def get_popular_demand(role, user, page, t1id, aid, asc_of_price, count_per_page):
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
        'pid__t2id__t1id',
        'aid__cid__pid',
        'pmid', 'wcid'
    ).filter(in_use=True, match=True).filter(
        end_time__gt=now()
    ).exclude(
        t_demand=t_demand_translator.from_role(role)
    )

    qs = hide_satisfied(qs)

    qs = filter_and_order_demand(qs, t1id, aid, asc_of_price)

    st, ed, n_pages = get_page_info(qs, count_per_page, page, index_error_excepiton=Error400("Page out of range"))

    # return sliced single page
    return qs[st:ed], n_pages


@default_exception(Error500)
@user_from_sid(Error404)
def get_my_demand(user, page, t1id, aid, asc_of_price, count_per_page):
    """
    TODO: using user_sid to get specified page
    :param user:
    :param page:
    :param t1id:
    :param aid:
    :param asc_of_price:
    :param count_per_page
    :return: 
    """

    qs = ProductDemand.objects.select_related(
        'uid__user_validate',
        'pid__t2id__t1id',
        'aid__cid__pid',
        'pmid', 'wcid'
    ).filter(uid=user, in_use=True)

    qs = hide_satisfied(qs)

    qs = filter_and_order_demand(qs, t1id, aid, asc_of_price)

    st, ed, n_pages = get_page_info(qs, count_per_page, page, index_error_excepiton=Error400("Page out of range"))
    # return sliced single page
    return qs[st:ed], n_pages


@default_exception(Error500)
@user_from_sid(Error404)
def get_matched_demand(user, id, page, order, asc, count_per_page):
    """
    :param user:
    :param id:
    :param page:
    :param order:
    :param count_per_page:
    :return:
    """

    def confirm_satisfied(self, other):
        # type: (ProductDemand, ProductDemand) -> bool
        return self.quantity > other.min_quantity

    def match_key(m_obj):
        # type: (ProductDemand) -> object
        if order == match_order_choice.SCORE:
            return demand.match_score(m_obj)["score_overall"]
        elif order == match_order_choice.QUANTITY:
            return m_obj.quantity_left()
        elif order == match_order_choice.PRICE:
            return m_obj.price

    try:
        demand = ProductDemand.objects.select_related(
            'uid__user_validate',
            'pid__t2id__t1id',
            'aid__cid__pid',
            'pmid', 'wcid'
        ).get(in_use=True, id=id, uid=user)
    except ProductDemand.DoesNotExist:
        raise Error404("No such demand.")

    match_queryset = ProductDemand.objects.select_related(
        'uid__user_validate',
        'pid__t2id__t1id',
        'aid__cid__pid',
        'pmid', 'wcid'
    ).filter(
        in_use=True,            # Must be in use
        match=True,
        pid=demand.pid,
        aid__cid__pid=demand.aid.cid.pid
    ).exclude(
        uid__role=user.role     # Exclude same role
    ).filter(
        end_time__gt=now(),
    )

    match_queryset = hide_satisfied(match_queryset)     # hide the demand which is satisfied

    # FIXME: Here we got a efficient issue, Every time user use this api, it will query the full set
    # of matched queryset. We must figure out how to fetch it by page, or ... cache it.
    matches = match_queryset.all()
    matches_list = [
        m for m in matches if confirm_satisfied(demand, m)
    ]
    matches_list.sort(key=match_key, reverse=not asc)

    st, ed, n_pages = get_page_info_list(
        matches_list, count_per_page, page, index_error_excepiton=Error400("Page out of range")
    )

    # Set the match field
    if not demand.match:
        demand.match = True
        demand.save()

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
            'pid__t2id__t1id',
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
    :return:
    """
    try:
        return ProductDemandPhoto.objects.get(id=id).demand_photo.path
    except ProductDemandPhoto.DoesNotExist:
        raise Error404("No such photo.")


def get_photo_by_dmid(dmid):
    # type: (int) -> string
    try:
        demand_obj = ProductDemand.objects.get(id=dmid)
    except ProductDemand.DoesNotExist:
        raise Error404("no such demand")
    photo = demand_obj.demand_photo.filter(inuse=True).order_by('-id').last()
    if photo is not None:
        return photo.demand_photo.path
    else:
        return demand_obj.pid.t2id.t1id.default_photo.path


@default_exception(Error500)
@user_from_sid(Error404)
def get_search_demand(user, page, keyword, t1id, aid, asc_of_price, count_per_page):
    qs = ProductDemand.objects.select_related(
        'uid__user_validate',
        'pid__t2id__t1id',
        'aid__cid__pid',
        'pmid', 'wcid'
    ).filter(Q(uid__user_validate__company__contains=keyword) | Q(uid__user_validate__contact=keyword) |
             Q(pid__tname3=keyword), in_use=True).exclude(uid__role=user.role)

    qs = hide_satisfied(qs)

    qs = filter_and_order_demand(qs, t1id, aid, asc_of_price)

    st, ed, n_pages = get_page_info(qs, count_per_page, page, index_error_excepiton=Error400("Page out of range"))
    # return sliced single page
    return qs[st:ed], n_pages
