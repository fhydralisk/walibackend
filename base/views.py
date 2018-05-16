import urllib
import json
import traceback
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.conf import settings
from django.http.response import HttpResponse
from base.exceptions import WLException


class WLAPIView(object):
    API_VERSION = "0.1"
    parser_classes = (JSONParser, )
    DEFAULT_VALIDATE_EXC_CODE = 400
    ERROR_HTTP_STATUS = False

    def generate_response(self, data, context):
        return Response(data={
            "response": dict(
                {"result": 200},
                **data
            ),
            "version": self.API_VERSION,
            "context": context
        })

    def get_request_obj(self, request, method=None):
        if method is None:
            method = request.method

        if method == "POST":
            try:
                context = request.data.get("context", None)
                data = request.data["data"]
                return data, context
            except KeyError:
                raise WLException(code=400, message="Request format incorrect, data field is missing.")
        elif method == "GET":
            objs = request.GET
            if "context" in objs:
                context = objs.pop("context")
                try:
                    context = json.loads(urllib.unquote(context))
                except ValueError:
                    context = None
            else:
                context = None

            data = objs
            return data, context
        else:
            raise WLException(code=500, message="Unexpected call of get request object method.")

    def validate_serializer(self, serializer, exc_code=None):

        def iterate_err(errors, parent_field, s_field_errors):
            for field, errs in errors.items():
                if isinstance(errs, dict):
                    iterate_err(errs, field + ".", s_field_errors)
                else:
                    for err in errs:
                        s_field_errors.append("%s%s: %s" % (parent_field, field, err))

        if not serializer.is_valid():
            field_errors = []
            iterate_err(serializer.errors, "", field_errors)

            raise WLException(message="Validation on request object failed, errors: %s" % ";".join(
                field_errors
            ), code=exc_code if exc_code is not None else self.DEFAULT_VALIDATE_EXC_CODE)

    def handle_exception(self, exc):
        if isinstance(exc, WLException):
            reason = exc.message
            code = exc.code
        else:
            if settings.DEBUG:
                traceback.print_exc()

            if settings.DEBUG:
                reason = "%s %s" % (str(exc.__class__), str(exc))
            else:
                reason = "Internal Error"

            code = 500
            # TODO: Log the detailed exception

        if self.ERROR_HTTP_STATUS:
            return HttpResponse(content=reason, status=code)
        else:
            return Response(data={
                "response": {
                    "result": code,
                    "reason": reason
                },
                "version": self.API_VERSION,
            })
