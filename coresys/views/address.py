from rest_framework.views import APIView
from base.views import WLAPIView
from coresys.models import CoreAddressArea, CoreAddressCity, CoreAddressProvince
from coresys.serializers.address_serializers import \
    CoreAddressAreaSerializer, CoreAddressCitySerializer, CoreAddressProvinceSerializer, CoreAddressProvinceFSerializer
from base.util.placeholder2exceptions import get_placeholder2exception

class GetProvinceView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        cseri = CoreAddressProvinceSerializer(CoreAddressProvince.objects.filter(in_use=True), many=True)
        return self.generate_response(data={"provinces": cseri.data}, context=context)


class GetCityView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        try:
            cseri = CoreAddressCitySerializer(CoreAddressCity.objects.filter(
                in_use=True,
            ), many=True)
            return self.generate_response(data={"cities": cseri.data}, context=context)
        except (KeyError, ValueError):
            raise get_placeholder2exception("core/address/city/ : expect pid")


class GetAreaView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        try:
            cseri = CoreAddressAreaSerializer(CoreAddressArea.objects.filter(
                in_use=True,
                cid=int(data["cid"])
            ), many=True)
            return self.generate_response(data={"areas": cseri.data}, context=context)
        except (KeyError, ValueError):
            raise get_placeholder2exception("core/address/area/ : expect cid")


class GetAllFView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        cseri = CoreAddressProvinceFSerializer(CoreAddressProvince.objects.filter(in_use=True), many=True)
        return self.generate_response(data={"provinces": cseri.data, "ver": 0.1}, context=context)
