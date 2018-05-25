from rest_framework.views import APIView
from base.views import WLAPIView
from paymentsys.serializers.dummy_payment_api import DummyPaymentSerializer
from paymentsys.funcs.receipt_manager import manager


class DummyPaymentCallbackView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        api_seri = DummyPaymentSerializer(data=data)
        self.validate_serializer(api_seri)
        manager.respond_receipt(**api_seri.validated_data)

        return self.generate_response(data={}, context=context)
