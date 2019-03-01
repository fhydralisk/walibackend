from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from demandsys.models import ProductDemand, ProductDemandPhoto, ProductQuality, ProductTypeL3
from demandsys.serializers.validators.address_submit import AddressChoiceValidator


class DemandPhotoSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductDemandPhoto
        fields = ('id', 'photo_desc', 'upload_date')
        extra_kwargs = {
            "upload_date": {
                "format": "%s"
            }
        }


class DemandReadableDisplaySerializer(serializers.ModelSerializer):

    company = serializers.ReadOnlyField(source='uid.user_validate.company')
    contact = serializers.ReadOnlyField(source='uid.user_validate.contact')
    t_user = serializers.ReadOnlyField(source='uid.user_validate.t_user')

    tname1 = serializers.ReadOnlyField(source='pid.t2id.t1id.tname1')
    t1id = serializers.ReadOnlyField(source='pid.t2id.t1id.id')
    tname2 = serializers.ReadOnlyField(source='pid.t2id.tname2')
    t2id = serializers.ReadOnlyField(source='pid.t2id.id')
    tname3 = serializers.ReadOnlyField(source='pid.tname3')
    t3id = serializers.ReadOnlyField(source='pid.id')
    pwcdesc = serializers.ReadOnlyField(source='wcid.pwcdesc')
    pmdesc = serializers.ReadOnlyField(source='pmid.opmdesc')

    area = serializers.ReadOnlyField(source='aid.area')
    city = serializers.ReadOnlyField(source='aid.cid.city')
    province = serializers.ReadOnlyField(source='aid.cid.pid.province')

    satisfied = serializers.SerializerMethodField()
    demand_photo_ids = serializers.PrimaryKeyRelatedField(read_only=True, many=True, source='demand_photo')
    demand_photos = DemandPhotoSerializers(read_only=True, many=True, source='demand_photo')
    pn = serializers.ReadOnlyField(source='uid.pn')

    class Meta:
        model = ProductDemand
        fields = (
            'id', 't_demand', 'price', 'quantity', 'min_quantity', 'match', 'end_time',
            'freight_payer', 'is_expired', 'description',
            'company', 'contact', 't_user',
            'tname1', 'tname2', 'tname3', 'pwcdesc', 'pmdesc',
            'area', 'city', 'province',
            'satisfied',
            'demand_photos', 'demand_photo_ids',
            't3id', 't2id', 't1id', 'wcid', 'pmid', 'aid',
            'street', 'expired_after_days',
            'st_time', 'last_modify_from_now',
            'pn'
        )

    def get_satisfied(self, obj):
        # type: (ProductDemand) -> float
        return obj.quantity - obj.quantity_left()


class DemandReadableDisplaySelfSerializer(DemandReadableDisplaySerializer):

    class Meta(DemandReadableDisplaySerializer.Meta):
        fields = DemandReadableDisplaySerializer.Meta.fields + ('comment',)


class DemandReadableDisplaySearchSerializer(DemandReadableDisplaySerializer):

    class Meta(DemandReadableDisplaySerializer.Meta):
        fields = DemandReadableDisplaySerializer.Meta.fields


class DemandReadableDisplayMatchSerializer(DemandReadableDisplaySerializer):
    def __init__(self, match_demand, *args, **kwargs):
        self.match_demand = match_demand
        super(DemandReadableDisplayMatchSerializer, self).__init__(*args, **kwargs)

    score = serializers.SerializerMethodField()

    class Meta(DemandReadableDisplaySerializer.Meta):
        fields = DemandReadableDisplaySerializer.Meta.fields + ('score', )

    def get_score(self, data):
        return self.match_demand.match_score(data)


class DemandPublishSerializer(serializers.ModelSerializer):

    duration = serializers.FloatField(default=100)
    min_quantity = serializers.FloatField(default=0)
    qid = serializers.PrimaryKeyRelatedField(queryset=ProductQuality.objects.all(), allow_null=True, default=None)
    pid = serializers.PrimaryKeyRelatedField(queryset=ProductTypeL3.objects.all(), allow_null=True, default=None)

    class Meta:
        model = ProductDemand
        fields = (
            'qid', 'pid', 'wcid', 'quantity', 'min_quantity',
            'price', 'duration', 'abid', 'aid',
            'street', 'description', 'comment', 'match', 'comment',
        )
        validators = [
            AddressChoiceValidator()
        ]

    def validate(self, attrs):
        if attrs.get('pid') is None and attrs.get('qid') is None:
            raise ValidationError(detail='Both pid and qid is None', code=400)

        return attrs


class DemandEditSerializer(serializers.ModelSerializer):

    min_quantity = serializers.FloatField(default=0)

    @property
    def root(self):
        """
        Returns the top-level serializer for this field.
        """
        root = self
        return root

    class Meta:
        model = ProductDemand
        fields = (
            'quantity', 'min_quantity',
            'price', 'duration', 'abid', 'aid',
            'street', 'description', 'comment', 'match', 'comment'
        )
        validators = [
            AddressChoiceValidator()
        ]
