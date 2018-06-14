from rest_framework.views import APIView
from base.views import WLAPIView

from demandsys.funcs.catalog import get_l1_2_3, get_water_content
from demandsys.serializers.catalog import ProductTypeSerializer, ProductWaterContentSerializer, ProductTypeFDictSerializer


class GetTreedProductTypeView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        l1_types = get_l1_2_3()
        wc = get_water_content()
        return self.generate_response(data={
            "product_types": ProductTypeSerializer(l1_types, many=True).data,
            "product_watercontents": ProductWaterContentSerializer(wc, many=True).data,
        }, context=context)


class GetFTreedProductTypeView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        l1_types = get_l1_2_3()
        wc = get_water_content()
        return self.generate_response(data={
            "product_types": ProductTypeFDictSerializer(l1_types, many=True).data,
            "product_watercontents": ProductWaterContentSerializer(wc, many=True).data,
        }, context=context)
