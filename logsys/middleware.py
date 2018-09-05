# coding=utf-8
from .models.api_log import ApiLog
from usersys.funcs.utils.sid_management import sid_getuser


class ApiMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_sid = request.GET.get('user_sid')
        url = request.get_full_path()
        visitor = sid_getuser(user_sid)
        if visitor:
            api_log = ApiLog(visitor=visitor, url=url)
        else:
            api_log = ApiLog(url=url)
        api_log.save()
        response = self.get_response(request)

        return response
