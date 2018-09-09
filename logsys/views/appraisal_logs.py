# coding=utf-8
from rest_framework.views import APIView
from base.views import WLAPIView
import logsys.serializers.log_api as log_api
import logsys.serializers.log_entry as log_entry
import logsys.funcs.log_appraisal as log_appraisal_funcs
import logsys.funcs.log_invite as log_invite_funcs


class ObtainAppraisalLogView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri_api = log_api.ObtainAppraisalLogSerializer(data=data)
        self.validate_serializer(seri_api)

        log_appr_entries = log_appraisal_funcs.obtain_appraisal_log(**seri_api.validated_data)

        seri_appr_log = log_entry.AppraisalLogSerializer(log_appr_entries)
        appr_logs = seri_appr_log.data

        if log_appr_entries:
            pass
        else:
            appr_logs = None

        log_invite_entries = log_invite_funcs.obtain_invite_log(**seri_api.validated_data)
        seri_invite_logs = log_entry.InviteLogSerializer(log_invite_entries, many=True)
        description = {}
        description['register'] = u'货品信息已由买方登记'
        description['finish'] = u'已完成，交易信息已由买方登记'
        description['cancel'] = u'买方取消'
        return self.generate_response(
            data={
                "description": description,
                "invite_logs": seri_invite_logs.data,
                "appr_logs": appr_logs
            },
            context=context
        )
