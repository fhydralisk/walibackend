from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from invitesys.model_choices.invite_enum import handle_method_choice, t_invite_choice
from .invite import InviteInfoSubmitSerializer


class _FlowHandleValidator(object):
    def __call__(self, attrs):
        if attrs["handle_method"] != handle_method_choice.ACCEPT:
            if "reason" not in attrs or attrs["reason"] is None:
                raise ValidationError("Reason field cannot be null.", 400)


class FlowHandleSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    handle_method = serializers.ChoiceField(choices=handle_method_choice.get_choices())
    reason = serializers.CharField(required=False)
    ivid = serializers.IntegerField()

    class Meta:
        validators = [
            _FlowHandleValidator()
        ]


class ObtainInviteSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    t_invite = serializers.ChoiceField(choices=t_invite_choice.get_choices())
    page = serializers.IntegerField(default=0)


class ObtainInviteDetailSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    ivid = serializers.IntegerField()


class PublishInviteSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    invite = InviteInfoSubmitSerializer()
