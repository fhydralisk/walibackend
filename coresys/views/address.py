from rest_framework.views import APIView
from base.views import WLAPIView
from base.exceptions import WLException
from coresys.models import CoreAddressArea, CoreAddressCity, CoreAddressProvince
from coresys.serializers.address_serializers import \
    CoreAddressAreaSerializer, CoreAddressCitySerializer, CoreAddressProvinceSerializer, CoreAddressProvinceFSerializer


class GetProvinceView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        cseri = CoreAddressProvinceSerializer(CoreAddressProvince.objects.all(), many=True)
        return self.generate_response(data={"provinces": cseri.data}, context=context)


class GetCityView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        try:
            cseri = CoreAddressCitySerializer(CoreAddressCity.objects.filter(pid=int(data["pid"])), many=True)
            return self.generate_response(data={"cities": cseri.data}, context=context)
        except (KeyError, ValueError):
            raise WLException(message="Expect pid", code=400)


class GetAreaView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        try:
            cseri = CoreAddressAreaSerializer(CoreAddressArea.objects.filter(cid=int(data["cid"])), many=True)
            return self.generate_response(data={"areas": cseri.data}, context=context)
        except (KeyError, ValueError):
            raise WLException(message="Expect cid", code=400)


class GetAllFView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        cseri = CoreAddressProvinceFSerializer(CoreAddressProvince.objects.all(), many=True)
        return self.generate_response(data={"provinces": cseri.data, "ver": 0.1}, context=context)
