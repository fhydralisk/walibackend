from rest_framework import serializers
from paymentsys.models import PaymentReceipt


class PaymentReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentReceipt
        fields = "__all__"
