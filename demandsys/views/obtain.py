import os

from rest_framework.views import APIView
from base.views import WLAPIView
from django.http.response import FileResponse
from django.conf import settings
from demandsys.serializers.demand_api import (
    ObtainDemandSerializer, ObtainDemandDetailSerializer, ObtainHotDemandSerializer, ObtainDemandMatchSerializer
)
from demandsys.serializers.demand import (
    DemandReadableDisplaySerializer, DemandReadableDisplayMatchSerializer, DemandReadableDisplaySelfSerializer
)
from demandsys.serializers.photo_api import GetPhotoSerializer
from demandsys.funcs.acquire import get_popular_demand, get_demand_detail, get_my_demand, get_specified_photo, get_matched_demand


# TODO: Move page size into settings
class ObtainHotView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainHotDemandSerializer(data=data)
        self.validate_serializer(seri)

        demands, n_pages = get_popular_demand(count_per_page=5, **seri.data)

        seri_demand = DemandReadableDisplaySerializer(demands, many=True)

        return self.generate_response(
            data={
                "hot_demands": seri_demand.data,
                "n_pages": n_pages,
            }, context=context
        )


class ObtainSelfView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainDemandSerializer(data=data)
        self.validate_serializer(seri)

        demands, n_pages = get_my_demand(count_per_page=5, **seri.data)

        seri_demand = DemandReadableDisplaySelfSerializer(demands, many=True)

        return self.generate_response(
            data={
                "self_demands": seri_demand.data,
                "n_pages": n_pages,
            }, context=context
        )


class ObtainDetailView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainDemandDetailSerializer(data=data)
        self.validate_serializer(seri)

        demand = get_demand_detail(**seri.data)

        seri_demand = DemandReadableDisplaySerializer(demand)

        return self.generate_response(
            data={
                "demand": seri_demand.data,
            }, context=context
        )


class ObtainPhotoDataView(WLAPIView, APIView):
    ERROR_HTTP_STATUS = True

    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = GetPhotoSerializer(data=data)
        self.validate_serializer(seri)

        photo_path = get_specified_photo(**seri.data)
        real_path = os.path.join(settings.BASE_DIR, photo_path)

        return FileResponse(open(real_path), content_type='image')


class ObtainMatchView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainDemandMatchSerializer(data=data)
        self.validate_serializer(seri)

        demand, matches, pages = get_matched_demand(count_per_page=5, **seri.data)

        seri_demand = DemandReadableDisplayMatchSerializer(match_demand=demand, instance=matches, many=True)

        return self.generate_response(
            data={
                "match_demands": seri_demand.data,
                "n_pages": pages,
            }, context=context
        )
