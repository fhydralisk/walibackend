from rest_framework import serializers
from demandsys.models import ProductTypeL3, ProductTypeL2, ProductTypeL1, ProductWaterContent, ProductQuality


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        filtered = data.filter(in_use=True)
        return super(FilteredListSerializer, self).to_representation(filtered)


class ProductWaterContentSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductWaterContent
        fields = ('id', 'pwcdesc')


class ProductQualitySerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductQuality
        fields = ('id', 'pqdesc')


class ProductTypeL3Serializer(serializers.ModelSerializer):

    product_qualities = ProductQualitySerializer(source='quality', many=True)

    def __init__(self, *args, **kwargs):
        nested = kwargs.pop("nested", True)
        super(ProductTypeL3Serializer, self).__init__(*args, **kwargs)

        if not nested:
            self.fields.pop('product_qualities')

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductTypeL3
        fields = ('id', 'tname3', 'product_qualities')


class ProductTypeL2Serializer(serializers.ModelSerializer):

    product_types_l3 = ProductTypeL3Serializer(source='product_l3', many=True)

    def __init__(self, *args, **kwargs):
        nested = kwargs.pop("nested", True)
        super(ProductTypeL2Serializer, self).__init__(*args, **kwargs)

        if not nested:
            self.fields.pop('product_types_l3')

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductTypeL2
        fields = ('id', 'tname2', 'product_types_l3')


class ProductTypeSerializer(serializers.ModelSerializer):

    product_types_l2 = ProductTypeL2Serializer(source='product_l2', many=True)

    def __init__(self, *args, **kwargs):
        nested = kwargs.pop("nested", True)
        super(ProductTypeSerializer, self).__init__(*args, **kwargs)

        if not nested:
            self.fields.pop('product_types_l2')

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductTypeL1
        fields = ('id', 'tname1', 'product_types_l2')