# coding=utf-8
from .models.api_log import ApiLog
from usersys.funcs.utils.sid_management import sid_getuser
import json


class ApiMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        string = ''
        parameter = request.GET.items()
        user_sid = None
        for (key, value) in parameter:
            string = string + str(key) + '=' + str(value) + ';'
        if method == 'GET':
            user_sid = request.GET.get('user_sid')
        elif method == 'POST':
            try:
                data = json.loads(request.body)['data']
                string += request.body
                user_sid = data['user_sid']
            except ValueError:
                string += 'Request format is incorrect or photo'
            except KeyError:
                user_sid = None
        else:
            pass
        url = request.path
        visitor = sid_getuser(user_sid)
        if visitor:
            api_log = ApiLog(visitor=visitor, url=url, parameter=string)
        else:
            api_log = ApiLog(url=url, parameter=string)
        api_log.save()
        response = self.get_response(request)

        return response
