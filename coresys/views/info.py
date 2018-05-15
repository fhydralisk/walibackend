from rest_framework.views import APIView
from base.views import WLAPIView
from coresys.models import CoreDistributionMethod, CorePaymentMethod
from coresys.serializers.distribution import CoreDistributionMethodSerializer
from coresys.serializers.payment import CorePaymentMethodSerializer


class CoreInfoPDView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri_pm = CorePaymentMethodSerializer(CorePaymentMethod.objects.filter(in_use=True), many=True)
        seri_dm = CoreDistributionMethodSerializer(CoreDistributionMethod.objects.filter(in_use=True), many=True)

        return self.generate_response(data={
            "pms": seri_pm.data,
            "dms": seri_dm.data,
        }, context=context)
