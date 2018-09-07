# coding=utf-8

import json
from django.http.response import HttpResponse

from .models.api_log import ApiLog
from usersys.funcs.utils.sid_management import sid_getuser


class ApiMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def record_api(url, user_sid, parameter):
        visitor = sid_getuser(user_sid) if user_sid is not None else None
        ApiLog.objects.create(visitor=visitor, url=url, parameter=parameter)

    def __call__(self, request):
        method = request.method
        url = request.path

        # TODO: Check whether url is our API, not admin site, etc.

        # Check method
        if method == 'GET':
            user_sid = request.GET.get('user_sid', None)

            try:
                parameter = json.dumps(request.GET)
            except ValueError:
                parameter = None

            self.record_api(url, user_sid, parameter)
        elif method == 'POST':
            content_type = request.content_type  # type: str
            if content_type.lower() == 'application/json':
                parameter = request.body
                try:
                    data = json.loads(request.body)
                    user_sid = data['data']['user_sid']
                except ValueError:
                    parameter += ' : Incorrect Json Format'
                    user_sid = None
                except KeyError:
                    user_sid = None
            else:
                # Maybe user_sid is in query string.
                user_sid = request.GET.get('user_sid', None)
                parameter = ''

            self.record_api(url, user_sid, parameter)
        else:
            pass

        response = self.get_response(request)  # type: HttpResponse

        return response
