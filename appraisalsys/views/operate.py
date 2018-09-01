from rest_framework.views import APIView
from base.views import WLAPIView
from appraisalsys.serializers.appraisal_api import (
    SubmitAppraisalSerializer,
)
from appraisalsys.serializers.appraisal import AppraisalSubmitDisplaySerializer
from appraisalsys.funcs.operate_appraisal import submit_appraisal


class SubmitAppraisalView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = SubmitAppraisalSerializer(data=data)
        self.validate_serializer(seri)

        appraisal = submit_appraisal(**seri.data)
        seri_appraisal = AppraisalSubmitDisplaySerializer(appraisal)

        return self.generate_response(
            data={
                "appraisal": seri_appraisal.data,
            },
            context=context
        )
