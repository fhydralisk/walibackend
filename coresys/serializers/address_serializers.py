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


class CoreAddressAreaFSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField(source='area')
    code = serializers.ReadOnlyField(source='id')

    class Meta:
        model = CoreAddressArea
        fields = ('name', 'code')


class CoreAddressCityFSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField(source='city')
    code = serializers.ReadOnlyField(source='id')
    sub = CoreAddressAreaFSerializer(many=True, source='area')

    class Meta:
        model = CoreAddressCity
        fields = ('name', 'code', 'sub')


class CoreAddressProvinceFSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField(source='province')
    code = serializers.ReadOnlyField(source='id')
    sub = CoreAddressCityFSerializer(many=True, source='city')

    class Meta:
        model = CoreAddressProvince
        fields = ('name', 'code', 'sub')

