from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.serializers.order_api import OperateOrderSerializer, OperateOrderProtocolSerializer
from ordersys.serializers.order import OrderInfoDisplaySerializer
from ordersys.funcs.operate_order import operate_order, operate_order_protocol


class OperateOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = OperateOrderSerializer(data=data)
        self.validate_serializer(seri)

        order = operate_order(**seri.data)

        return self.generate_response(data={
            "order": OrderInfoDisplaySerializer(order).data
        }, context=context)


class OperateProtocolView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = OperateOrderProtocolSerializer(data=data)
        self.validate_serializer(seri)

        operate_order_protocol(**seri.data)

        return self.generate_response(data={}, context=context)
