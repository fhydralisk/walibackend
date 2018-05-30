from rest_framework import serializers
from coresys.models import CoreDistributionMethod


class CoreDistributionMethodSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='odmdesc')

    class Meta:
        model = CoreDistributionMethod
        exclude = ('in_use', )
