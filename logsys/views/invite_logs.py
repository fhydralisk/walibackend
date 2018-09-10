# coding=utf-8
from rest_framework.views import APIView
from base.views import WLAPIView
import logsys.serializers.log_api as log_api
import logsys.serializers.log_invite_entry as log_entry
import logsys.funcs.log_invite as log_invite_funcs


class ObtainInviteLogView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri_api = log_api.ObtainInviteLogSerializer(data=data)
        self.validate_serializer(seri_api)

        invite, user = log_invite_funcs.check_invite_user(**seri_api.validated_data)

        return self.generate_response(
            data=log_entry.InviteAndAppraisalLogSerializer(user=user, instance=invite).data,
            context=context
        )
