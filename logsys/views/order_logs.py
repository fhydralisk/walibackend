from rest_framework.views import APIView
from base.views import WLAPIView
import logsys.serializers.log_api as log_api
import logsys.serializers.log_entry as log_entry
import logsys.funcs.log_order as log_order_funcs


class ObtainLogOrderStatusView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri_api = log_api.ObtainOrderLogSerializer(data=data)
        self.validate_serializer(seri_api)

        log_entries = log_order_funcs.obtain_order_log(**seri_api.validated_data)

        seri_log = log_entry.OrderLogSerializer(log_entries, many=True)

        return self.generate_response(
            data={
                "logs": seri_log.data
            },
            context=context
        )


class ObtainLogOrderProtocolStatusView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri_api = log_api.ObtainOrderProtocolLogSerializer(data=data)
        self.validate_serializer(seri_api)

        log_entries = log_order_funcs.obtain_order_protocol_log(**seri_api.validated_data)

        seri_log = log_entry.OrderProtocolLogSerializer(log_entries, many=True)

        return self.generate_response(
            data={
                "logs": seri_log.data
            },
            context=context
        )
