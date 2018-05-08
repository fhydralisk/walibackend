
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.conf import settings
from base.exceptions import WLException


class WLAPIView(object):
    API_VERSION = "0.1"
    parser_classes = (JSONParser, )
    DEFAULT_VALIDATE_EXC_CODE = 400

    def generate_response(self, data, context):
        return Response(data={
            "response": dict(
                {"result": 200},
                **data
            ),
            "version": self.API_VERSION,
            "context": context
        })

    def get_request_obj(self, request):
        try:
            context = request.data.get("context", None)
            data = request.data["data"]
            return data, context
        except KeyError:
            raise WLException(code=400, message="Request format incorrect, data field is missing.")

    def validate_serializer(self, serializer, exc_code=None):
        if not serializer.is_valid():
            raise WLException(message="Validation on request object failed, errors: %s" % ";".join(
                map(lambda x: str(x), serializer.errors)
            ), code=exc_code if exc_code is not None else self.DEFAULT_VALIDATE_EXC_CODE)

    def handle_exception(self, exc):
        if isinstance(exc, WLException):
            return Response(data={
                "response": {
                    "result": exc.code,
                    "reason": exc.message
                },
                "version": self.API_VERSION,
            })
        else:
            if settings.DEBUG:
                print("Unhandled Exception: %s" % str(exc))
            # TODO: Log the detailed exception
            return Response(data={
                "response": {
                    "result": 500,
                    "reason": "Internal Error"
                },
                "version": self.API_VERSION,
            })
