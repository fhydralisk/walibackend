from rest_framework.views import APIView
from base.views import WLAPIView
from simplified_invite.serializers.simplified_invite_api import (
    SubmitInviteSerializer, CancelInviteSerializer
)
from simplified_invite.serializers.invite import InviteInfoDisplaySerializer
from simplified_invite.funcs.invite import submit_invite, cancel_invite


class SubmitInviteView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = SubmitInviteSerializer(data=data)

        self.validate_serializer(seri)
        iv = submit_invite(**seri.validated_data)
        seri_invite = InviteInfoDisplaySerializer(iv)

        return self.generate_response(
            data={
                "invite": seri_invite.data
            },
            context=context
        )


class CancelInviteView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = CancelInviteSerializer(data=data)
        self.validate_serializer(seri)
        cancel_invite(**seri.data)
        return self.generate_response(
            data={},
            context=context
        )
