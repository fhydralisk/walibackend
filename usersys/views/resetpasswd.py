from rest_framework.views import APIView
from base.views import WLAPIView

from usersys.serializers.register_api import ResetPasswordSerializer
from usersys.funcs.registration import validate_sid
from usersys.funcs.modify_password import modify_password


class ResetPasswordView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = ResetPasswordSerializer(data=data)
        self.validate_serializer(seri)

        validate_kwargs = {k: v for k, v in seri.data.items()}
        del validate_kwargs["password"]
        del validate_kwargs["role"]

        modify_password_kwargs = {k: v for k, v in seri.data.items()}
        del modify_password_kwargs["vcode"]

        validate_sid(**validate_kwargs)

        modify_password(**modify_password_kwargs)

        return self.generate_response(data={
            "pn": seri.data["pn"]
        }, context=context)
