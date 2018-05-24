from rest_framework import serializers
from ordersys.models import OrderInfo
from paymentsys.models import PaymentReceipt


class DummyPaymentContextSerializer(serializers.Serializer):
    r_type = serializers.ChoiceField(choices=("refund", "payment"))
    oid = serializers.PrimaryKeyRelatedField(queryset=OrderInfo.objects)


class DummyPaymentSerializer(serializers.Serializer):
    receipt = serializers.SlugRelatedField(queryset=PaymentReceipt.objects, slug_field="receipt_number")
    response = DummyPaymentContextSerializer()
