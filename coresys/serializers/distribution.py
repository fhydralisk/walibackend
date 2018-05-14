from rest_framework import serializers
from coresys.models import CoreDistributionMethod


class CoreDistributionMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoreDistributionMethod
        exclude = ('in_use', )
