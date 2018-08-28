from rest_framework.views import APIView
from base.views import WLAPIView

from usersys.serializers.user_info import UserInfoSerialzier
from usersys.funcs.info import get_user_info
from base.exceptions import WLException
from usersys.serializers.search_api import (
    GetSearchHistoryApiSerializer, SearchHistoryInfoSerializer
)
from usersys.funcs.search_history import get_search_history, empty_search_history


class UserInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        if "user_sid" not in data:
            raise WLException(message="Bad Request", code=400)
        user = get_user_info(user_sid=data["user_sid"])
        useri = UserInfoSerialzier(user)
        return self.generate_response(data=useri.data, context=context)


class GetSearchHistoryView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = GetSearchHistoryApiSerializer(data=data)
        self.validate_serializer(seri)
        search_history = get_search_history(**seri.validated_data)
        search_history_seri = SearchHistoryInfoSerializer(search_history, many=True)
        return self.generate_response(data={"search_history": search_history_seri.data}, context=context)


class EmptySearchHistoryView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = GetSearchHistoryApiSerializer(data=data)
        self.validate_serializer(seri)
        empty_search_history(**seri.validated_data)
        return self.generate_response(data={}, context=context)
