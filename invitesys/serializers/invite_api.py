from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from coresys.models import CorePaymentMethod
from usersys.funcs.utils.sid_management import sid_getuser
from usersys.model_choices.user_enum import role_choice
from invitesys.model_choices.invite_enum import handle_method_choice, t_invite_choice
from invitesys.models import InviteCancelReason
from .invite import BuyerInviteInfoSubmitSerializer, SellerInviteInfoSubmitSerializer


def check_attr_exist(attrs, field, err_message, err_code):
    if field not in attrs or attrs[field] is None:
        raise ValidationError({field: err_message}, err_code)


class FlowHandleSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    handle_method = serializers.ChoiceField(choices=handle_method_choice.get_choices())
    reason = serializers.CharField(required=False)
    reason_class = serializers.PrimaryKeyRelatedField(queryset=InviteCancelReason.objects.all(), required=False)
    price = serializers.FloatField(min_value=0.01, required=False)
    pmid = serializers.PrimaryKeyRelatedField(queryset=CorePaymentMethod.objects.filter(in_use=True), required=False)
    ivid = serializers.IntegerField()

    def validate(self, attrs):
        handle_method = attrs["handle_method"]
        if handle_method in (handle_method_choice.CANCEL, handle_method_choice.REJECT):
            check_attr_exist(attrs, "reason", "This filed is required", 400)
            check_attr_exist(attrs, "reason_class", "This field is required", 400)

        elif handle_method == handle_method_choice.NEGOTIATE:
            check_attr_exist(attrs, "price", "This field is required", 400)
            check_attr_exist(attrs, "pmid", "This field is required", 400)

        return attrs


class ObtainInviteSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    t_invite = serializers.ChoiceField(choices=t_invite_choice.get_choices())
    page = serializers.IntegerField(default=0)


class ObtainInviteDetailSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    ivid = serializers.IntegerField()


class PublishInviteSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    invite = serializers.JSONField()

    def validate(self, attrs):
        user = sid_getuser(attrs["user_sid"])
        if user is None:
            raise ValidationError({"user_sid": ["No such user"]})

        if user.role == role_choice.BUYER:
            seri_cls = BuyerInviteInfoSubmitSerializer

        elif user.role == role_choice.SELLER:
            seri_cls = SellerInviteInfoSubmitSerializer

        else:
            raise ValidationError({"user_sid": ["Role of user is invalid"]})

        seri = seri_cls(data=attrs["invite"])
        seri.is_valid(raise_exception=True)

        attrs["invite"] = seri.validated_data
        return attrs


class InviteCancelReasonDisplaySerializer(serializers.ModelSerializer):

    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='reason')

    class Meta:
        model = InviteCancelReason
        fields = ('value', 'label')
