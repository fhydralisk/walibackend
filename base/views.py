import urllib
import json
import logging
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import MethodNotAllowed
from django.http.response import HttpResponseNotAllowed
from django.conf import settings
from django.http.response import HttpResponse
from base.exceptions import WLException
from base.util.serializer_helper import errors_summery


logger = logging.getLogger(__name__)


class WLAPIView(object):
    API_VERSION = "0.1"
    parser_classes = (JSONParser, )
    DEFAULT_VALIDATE_EXC_CODE = 400
    ERROR_HTTP_STATUS = False
    http_method_names = ['get', 'post', 'options']

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

        if not serializer.is_valid():
            message = errors_summery(serializer)

            raise WLException(
                message=message,
                code=exc_code if exc_code is not None else self.DEFAULT_VALIDATE_EXC_CODE
            )

    def handle_exception(self, exc):
        if isinstance(exc, WLException):
            reason = exc.message
            code = exc.code
            if exc.code == 500:
                logger.exception("WLException 500", extra={"request": self.request})
            else:
                logger.warn("WLException: %d, %s" % (code, reason), extra={"request": self.request})
        elif isinstance(exc, MethodNotAllowed):
            return HttpResponseNotAllowed(self.http_method_names)
        else:
            if settings.DEBUG:
                reason = "%s %s" % (str(exc.__class__), str(exc))
            else:
                reason = "Internal Error"

            code = 500
            # Log the detailed exception
            logger.exception("Exception not handled", extra={"request": self.request})

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
