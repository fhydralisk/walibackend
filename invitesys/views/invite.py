from rest_framework.views import APIView
from base.views import WLAPIView
from invitesys.serializers.invite_display import InviteReadableDisplaySerializer, InviteReadableDetailDisplaySerializer
from invitesys.serializers.invite_api import (
    FlowHandleSerializer, ObtainInviteSerializer, ObtainInviteDetailSerializer,
    PublishInviteSerializer
)
from invitesys.funcs.invites import handle, obtain, detail, publish


class FlowHandleView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)

        seri = FlowHandleSerializer(data=data)
        self.validate_serializer(seri)
        handle(**seri.data)

        return self.generate_response(data={}, context=context)


class ObtainInviteView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainInviteSerializer(data=data)
        self.validate_serializer(seri)
        # FIXME: count_pre_count should be move to settings or somewhere
        invites, n_pages = obtain(count_pre_page=5, **seri.data)

        seri_invites = InviteReadableDisplaySerializer(invites, many=True)

        return self.generate_response(
            data={
                "invites": seri_invites.data,
                "n_pages": n_pages
            },
            context=context
        )


class ObtainInviteDetailView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainInviteDetailSerializer(data=data)
        self.validate_serializer(seri)
        iv = detail(**seri.data)
        seri_invite = InviteReadableDetailDisplaySerializer(iv)

        return self.generate_response(
            data={
                "invite": seri_invite.data
            },
            context=context
        )


class PublishInviteView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)

        seri = PublishInviteSerializer(data=data)
        self.validate_serializer(seri)
        iv = publish(**seri.validated_data)
        seri_invite = InviteReadableDetailDisplaySerializer(iv)

        return self.generate_response(
            data={
                "invite": seri_invite.data
            },
            context=context
        )

