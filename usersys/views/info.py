from rest_framework.views import APIView
from base.views import WLAPIView

from usersys.serializers.user_info_serializer import UserInfoSerialzier
from usersys.funcs.info import get_user_info
from base.exceptions import WLException


class UserInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        if "user_sid" not in data:
            raise WLException(message="Bad Request", code=400)
        user = get_user_info(data["user_sid"])
        useri = UserInfoSerialzier(user)
        return self.generate_response(data=useri.data, context=context)
