from rest_framework.views import APIView
from base.views import WLAPIView

from usersys.serializers.user_info import UserInfoSerialzier
from usersys.funcs.info import get_user_info
from base.exceptions import WLException
from usersys.funcs.placeholder2exceptions import get_placeholder2exception


class UserInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        if "user_sid" not in data:
            raise get_placeholder2exception("user/info/self/ : user_sid not in url")
        user = get_user_info(user_sid=data["user_sid"])
        useri = UserInfoSerialzier(user)
        return self.generate_response(data=useri.data, context=context)
