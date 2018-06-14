from rest_framework import serializers
from demandsys.models import ProductTypeL3, ProductTypeL2, ProductTypeL1, ProductWaterContent, ProductQuality


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        filtered = data.filter(in_use=True)
        return super(FilteredListSerializer, self).to_representation(filtered)


class ProductWaterContentSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='pwcdesc')

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductWaterContent
        fields = ('value', 'label')


class ProductQualitySerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='pqdesc')

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductQuality
        fields = ('value', 'label')


class ProductTypeL3Serializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='tname3')
    product_qualities = ProductQualitySerializer(source='quality', many=True)

    def __init__(self, *args, **kwargs):
        nested = kwargs.pop("nested", True)
        super(ProductTypeL3Serializer, self).__init__(*args, **kwargs)

        if not nested:
            self.fields.pop('product_qualities')

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductTypeL3
        fields = ('value', 'label', 'product_qualities')


class ProductTypeL2Serializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='tname2')
    product_types_l3 = ProductTypeL3Serializer(source='product_l3', many=True)

    def __init__(self, *args, **kwargs):
        nested = kwargs.pop("nested", True)
        super(ProductTypeL2Serializer, self).__init__(*args, **kwargs)

        if not nested:
            self.fields.pop('product_types_l3')

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductTypeL2
        fields = ('value', 'label', 'product_types_l3')


class ProductTypeSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='tname1')
    product_types_l2 = ProductTypeL2Serializer(source='product_l2', many=True)

    def __init__(self, *args, **kwargs):
        nested = kwargs.pop("nested", True)
        super(ProductTypeSerializer, self).__init__(*args, **kwargs)

        if not nested:
            self.fields.pop('product_types_l2')

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductTypeL1
        fields = ('value', 'label', 'product_types_l2')


class ProductQualityFDictSerializer(serializers.ModelSerializer):
    code = serializers.ReadOnlyField(source='id')
    name = serializers.ReadOnlyField(source='pqdesc')

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductQuality
        fields = ('code', 'name')


class ProductTypeL3FDictSerializer(serializers.ModelSerializer):
    code = serializers.ReadOnlyField(source='id')
    name = serializers.ReadOnlyField(source='tname3')
    sub = ProductQualityFDictSerializer(source='quality', many=True)

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductTypeL3
        fields = ('code', 'name', 'sub')


class ProductTypeL2FDictSerializer(serializers.ModelSerializer):
    code = serializers.ReadOnlyField(source='id')
    name = serializers.ReadOnlyField(source='tname2')
    sub = ProductTypeL3FDictSerializer(source='product_l3', many=True)

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductTypeL2
        fields = ('code', 'name', 'sub')


class ProductTypeFDictSerializer(serializers.ModelSerializer):
    code = serializers.ReadOnlyField(source='id')
    name = serializers.ReadOnlyField(source='tname1')
    sub = ProductTypeL2FDictSerializer(source='product_l2', many=True)

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ProductTypeL1
        fields = ('code', 'name', 'sub')
