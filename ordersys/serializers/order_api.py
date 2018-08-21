from rest_framework import serializers
from ordersys.model_choices.order_enum import (
    o_buyer_action_choice, o_seller_action_choice, order_type_choice, op_buyer_action_choice, op_seller_action_choice
)
from ordersys.serializers.distribution import OrderLogisticsInfoSubmitSerializer
from ordersys.serializers.order import OrderProtocolSubmitSerializer
from paymentsys.models import PaymentPlatform


class PaymethodSerializer(serializers.Serializer):
    paymethod = serializers.PrimaryKeyRelatedField(queryset=PaymentPlatform.objects)


class SubmitLogisticsSerializer(serializers.Serializer):
    loginfo = OrderLogisticsInfoSubmitSerializer()


class SubmitProtocolSerializer(serializers.Serializer):
    protocol = OrderProtocolSubmitSerializer()


class ReasonSerializer(serializers.Serializer):
    reason = serializers.CharField()


class OperateOrderSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    oid = serializers.IntegerField()
    action = serializers.ChoiceField(choices=o_buyer_action_choice.get_choices()+o_seller_action_choice.get_choices())
    parameter = serializers.JSONField(required=False)

    def validate(self, data):
        action = data["action"]
        seri_class = None

        if action in (
                o_seller_action_choice.SELLER_APPEND_RECEIPT_LOGISTICS,
                o_seller_action_choice.SELLER_APPEND_RECEIPT_LOGISTICS
        ):
            seri_class = SubmitLogisticsSerializer

        if action == o_buyer_action_choice.BUYER_SUBMIT_PROTOCOL:
            seri_class = SubmitProtocolSerializer

        if action == o_seller_action_choice.SELLER_REJECT_PROTOCOL:
            seri_class = ReasonSerializer

        if seri_class is not None:
            seri = seri_class(data=data.get("parameter", {}))
            seri.is_valid(raise_exception=True)

        return data


class OperateOrderProtocolSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    oid = serializers.IntegerField()
    action = serializers.ChoiceField(choices=(
            op_buyer_action_choice.get_choices()+op_seller_action_choice.get_choices()
    ))
    parameter = serializers.JSONField(required=False)

    def validate(self, data):
        action = data["action"]
        seri_class = None
        if action == op_buyer_action_choice.BUYER_PAY_FINAL:
            seri_class = PaymethodSerializer

        if action == op_buyer_action_choice.CANCEL_APPEND_LOGISTICS_INFO:
            seri_class = SubmitLogisticsSerializer

        if seri_class is not None:
            seri = seri_class(data=data.get("parameter", {}))
            seri.is_valid(raise_exception=True)

        return data


class ObtainOrderListSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    order_type = serializers.ChoiceField(choices=order_type_choice.get_choices())
    page = serializers.IntegerField(default=0)


class ObtainOrderSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    oid = serializers.IntegerField()

