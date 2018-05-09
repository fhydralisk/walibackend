from rest_framework import serializers
from coresys.models import CoreAddressProvince, CoreAddressCity, CoreAddressArea


class CoreAddressProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoreAddressProvince
        fields = '__all__'


class CoreAddressCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CoreAddressCity
        fields = '__all__'


class CoreAddressAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoreAddressArea
        fields = '__all__'
