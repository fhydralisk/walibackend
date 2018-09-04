from rest_framework.views import APIView
from base.views import WLAPIView
from simplified_invite.serializers.simplified_invite_api import (
    ObtainDefaultInviteSerializer, ObtainSelfInvite2AppraisalSerializer, ObtainInvite2AppraisalDetailSerializer
)
from simplified_invite.serializers.invite import (
    DefaultInviterInfoSerializer, SelfInviteDisplaySerializer, InviteDetailDisplaySerializer
)
from simplified_invite.funcs.obtain_invite_to_appraisal import demand_to_invite
from simplified_invite.funcs.obtain_invite_to_appraisal import obtain_self_invite2appraisal_list, obtain_invite2appraisal_detail


class ObtainDefaultInviteView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainDefaultInviteSerializer(data=data)
        self.validate_serializer(seri)

        invite = demand_to_invite(**seri.data)
        seri_invite = DefaultInviterInfoSerializer(invite)
        return self.generate_response(
            data={
                "default_invites": seri_invite.data
            },
            context=context
        )


class ObtainInvite2SelfAppraisalView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainSelfInvite2AppraisalSerializer(data=data)
        self.validate_serializer(seri)

        invite, n_pages = obtain_self_invite2appraisal_list(count_per_page=5, **seri.data)
        seri_invites = SelfInviteDisplaySerializer(invite, many=True)

        return self.generate_response(
            data={
                "self_invites": seri_invites.data,
                "n_pages":  n_pages
            },
            context=context
        )


class ObtainInvite2AppraisalSDetailView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainInvite2AppraisalDetailSerializer(data=data)
        self.validate_serializer(seri)

        invite = obtain_invite2appraisal_detail(**seri.data)
        seri_invite = InviteDetailDisplaySerializer(invite)

        return self.generate_response(
            data={
                "invite_detail": seri_invite.data
            },
            context=context
        )
