from rest_framework import serializers
from coresys.models import CorePaymentMethod


class CorePaymentMethodSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='opmdesc')

    class Meta:
        model = CorePaymentMethod
        exclude = ('in_use', )
