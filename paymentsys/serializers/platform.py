from rest_framework import serializers
from paymentsys.models import PaymentPlatform


class PaymentPlatformIDPlatform(serializers.ModelSerializer):

    class Meta:
        model = PaymentPlatform
