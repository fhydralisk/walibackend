from rest_framework.views import APIView
from base.views import WLAPIView
from base.util.get_ip import get_client_ip
from usersys.serializers.login_api_serializers import LoginSerializer, LogoutSerializer
from usersys.funcs.login import login, logout


class LoginView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = LoginSerializer(data=data)
        self.validate_serializer(seri)

        sid = login(ipaddr=get_client_ip(request), **seri.data)
        return self.generate_response(data={
            "pn": seri.data["pn"],
            "user_sid": sid
        }, context=context)


class LogoutView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = LogoutSerializer(data=data)
        self.validate_serializer(seri)

        logout(**seri.data)
        return self.generate_response(data={}, context=context)
