from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.serializers.order_api import ObtainOrderSerializer, ObtainOrderListSerializer
from ordersys.serializers.order import OrderInfoDisplaySerializer
from ordersys.funcs.obtain_order import obtain_order_detail, obtain_order_list


class ObtainOrderView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainOrderListSerializer(data=data)
        self.validate_serializer(seri)
        # FIXME: count_pre_count should be move to settings or somewhere
        orders, n_pages = obtain_order_list(count_pre_page=5, **seri.data)

        seri_orders = OrderInfoDisplaySerializer(orders, many=True)

        return self.generate_response(
            data={
                "orders": seri_orders.data,
                "n_pages": n_pages
            },
            context=context
        )


class ObtainOrderDetailView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainOrderSerializer(data=data)
        self.validate_serializer(seri)
        iv = obtain_order_detail(**seri.data)
        seri_order = OrderInfoDisplaySerializer(iv)

        return self.generate_response(
            data={
                "order": seri_order.data
            },
            context=context
        )
