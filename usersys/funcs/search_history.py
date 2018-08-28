from base.exceptions import default_exception, Error500, Error404
from utils.usersid import user_from_sid
from usersys.models import SearchHistory

@default_exception(Error500)
@user_from_sid(Error404)
def submit_search_history(user, keyword):
    try:
        SearchHistory.objects.get(keyword=keyword)
    except SearchHistory.DoesNotExist:
        SearchHistory.objects.create(
            uid=user,
            keyword=keyword,
        )


@default_exception(Error500)
@user_from_sid(Error404)
def get_search_history(user):
    search_history_query =  SearchHistory.objects.filter(uid=user).order_by('-id')
    if len(search_history_query) >= 10:
        return search_history_query[:10]
    else:
        return search_history_query
    # return search_history_query

@default_exception(Error500)
@user_from_sid(Error404)
def empty_search_history(user):
    SearchHistory.objects.filter(uid=user).delete()