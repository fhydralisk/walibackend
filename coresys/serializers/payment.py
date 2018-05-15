from rest_framework import serializers
from coresys.models import CorePaymentMethod


class CorePaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = CorePaymentMethod
        exclude = ('in_use', )
