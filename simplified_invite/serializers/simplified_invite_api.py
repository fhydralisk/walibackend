from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from usersys.funcs.utils.sid_management import sid_getuser
from usersys.model_choices.user_enum import role_choice
from simplified_invite.model_choices.invite_enum import t_invite_choice
from simplified_invite.serializers.invite import InviteInfoInAppraisalSysSubmitSerializer


class ObtainDefaultInviteSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    dmid = serializers.IntegerField()


class ObtainSelfInvite2AppraisalSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    t_invite = serializers.ChoiceField(choices=t_invite_choice.get_choices())
    page = serializers.IntegerField(default=0)


class ObtainInvite2AppraisalDetailSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    ivid = serializers.IntegerField()


class SubmitInviteSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    invite = serializers.JSONField()

    def validate(self, attrs):
        user = sid_getuser(attrs["user_sid"])
        if user is None:
            raise ValidationError({"user_sid": ["No such user"]})

        if not user.role == role_choice.BUYER:
            raise ValidationError({"user_sid": ["Role of user is invalid"]})

        seri_cls = InviteInfoInAppraisalSysSubmitSerializer

        seri = seri_cls(data=attrs["invite"])
        seri.is_valid(raise_exception=True)
        attrs["invite"] = seri.validated_data
        return attrs


class CancelInviteSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    ivid = serializers.IntegerField()
    reason_id = serializers.IntegerField()
    reason = serializers.CharField(max_length=256, default=None, allow_null=True)
