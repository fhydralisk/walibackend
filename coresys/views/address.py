from rest_framework.views import APIView
from base.views import WLAPIView
from coresys.models import CoreAddressCity, CoreAddressProvince
from coresys.serializers.address_serializers import \
    CoreAddressAreaSerializer, CoreAddressCitySerializer, CoreAddressProvinceSerializer, CoreAddressProvinceFSerializer
from coresys.funcs.placeholder2exceptions import get_placeholder2exception


class GetProvinceView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        cseri = CoreAddressProvinceSerializer(CoreAddressProvince.objects.filter(in_use=True), many=True)
        return self.generate_response(data={"provinces": cseri.data}, context=context)


class GetCityView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        try:
            cseri = CoreAddressCitySerializer(CoreAddressProvince.objects.get(id=int(data["pid"])).city.filter(
                in_use=True,
            ), many=True)
            return self.generate_response(data={"cities": cseri.data}, context=context)
        except (KeyError, ValueError):
            raise get_placeholder2exception("core/address/city/ : expect pid")
        except CoreAddressProvince.DoesNotExist:
            raise get_placeholder2exception("core/address/city/ : pid not exist")


class GetAreaView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        try:
            cseri = CoreAddressAreaSerializer(CoreAddressCity.objects.get(id=int(data["cid"])).area.filter(
                in_use=True
            ), many=True)
            return self.generate_response(data={"areas": cseri.data}, context=context)
        except (KeyError, ValueError):
            raise get_placeholder2exception("core/address/area/ : expect cid")
        except CoreAddressCity.DoesNotExist:
            raise get_placeholder2exception("core/address/area/ : cit not exist")


class GetAllFView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        cseri = CoreAddressProvinceFSerializer(CoreAddressProvince.objects.filter(in_use=True), many=True)
        return self.generate_response(data={"provinces": cseri.data, "ver": 0.1}, context=context)
