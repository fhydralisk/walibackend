from django.http.response import FileResponse
from django.conf import settings
from rest_framework.views import APIView
from base.views import WLAPIView


class RegisterProtocolView(WLAPIView, APIView):
    def get(self, request):
        f = open(settings.USE_PROTOCOL, 'r')
        return FileResponse(f, content_type='text/plain; charset=utf-8')
