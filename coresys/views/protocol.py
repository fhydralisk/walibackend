from django.http.response import FileResponse
from django.conf import settings
from rest_framework.views import APIView
from base.views import WLAPIView


class RegisterProtocolView(WLAPIView, APIView):
    def get(self, request):
        with open(settings.USE_PROTOCOL, 'r') as f:
            return self.generate_response(data={"content": f.read()}, context=None)
