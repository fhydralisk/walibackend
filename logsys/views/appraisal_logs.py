from rest_framework.views import APIView
from base.views import WLAPIView
import logsys.serializers.log_api as log_api
import logsys.serializers.log_entry as log_entry
import logsys.funcs.log_appraisal as log_appraisal_funcs


class ObtainAppraisalLogView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri_api = log_api.ObtainAppraisalLogSerializer(data=data)
        self.validate_serializer(seri_api)

        log_entries = log_appraisal_funcs.obtain_appraisal_log(**seri_api.validated_data)

        seri_log = log_entry.AppraisalLogSerializer(log_entries, many=True)

        appr_status = 0
        if seri_log.data:
            appr_status = 1

        return self.generate_response(
            data={
                "appr_status": appr_status,
                "logs": seri_log.data
            },
            context=context
        )
