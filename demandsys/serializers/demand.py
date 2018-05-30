from rest_framework import serializers
from demandsys.models import ProductDemand, ProductDemandPhoto
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

    tname1 = serializers.ReadOnlyField(source='qid.t3id.t2id.t1id.tname1')
    tname2 = serializers.ReadOnlyField(source='qid.t3id.t2id.tname2')
    tname3 = serializers.ReadOnlyField(source='qid.t3id.tname3')
    pqdesc = serializers.ReadOnlyField(source='qid.pqdesc')
    pwcdesc = serializers.ReadOnlyField(source='wcid.pwcdesc')
    pmdesc = serializers.ReadOnlyField(source='pmid.opmdesc')

    area = serializers.ReadOnlyField(source='aid.area')
    city = serializers.ReadOnlyField(source='aid.cid.city')
    province = serializers.ReadOnlyField(source='aid.cid.pid.province')

    satisfied = serializers.SerializerMethodField()
    demand_photo_ids = serializers.PrimaryKeyRelatedField(read_only=True, many=True, source='demand_photo')
    demand_photos = DemandPhotoSerializers(read_only=True, many=True, source='demand_photo')

    class Meta:
        model = ProductDemand
        fields = (
            'id', 't_demand', 'price', 'quantity', 'min_quantity', 'unit', 'match', 'end_time',
            'is_expired', 'description',
            'company', 'contact', 't_user',
            'tname1', 'tname2', 'tname3', 'pqdesc', 'pwcdesc', 'pmdesc',
            'area', 'city', 'province',
            'satisfied',
            'demand_photos', 'demand_photo_ids'
        )

    def get_satisfied(self, obj):
        # type: (ProductDemand) -> float
        return (obj.quantity_metric() - obj.quantity_left()).quantity


class DemandReadableDisplaySelfSerializer(DemandReadableDisplaySerializer):

    class Meta(DemandReadableDisplaySerializer.Meta):
        fields = DemandReadableDisplaySerializer.Meta.fields + ('comment', 'street',)


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

    duration = serializers.FloatField(min_value=0.0)

    class Meta:
        model = ProductDemand
        fields = (
            'qid', 'wcid', 'quantity', 'min_quantity',
            'price', 'unit', 'pmid', 'duration', 'abid', 'aid',
            'street', 'description', 'comment', 'match', 'comment'
        )
        validators = [
            AddressChoiceValidator()
        ]


class DemandEditSerializer(serializers.ModelSerializer):

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
            'price', 'unit', 'pmid', 'duration', 'abid', 'aid',
            'street', 'description', 'comment', 'match', 'comment',
        )
        validators = [
            AddressChoiceValidator()
        ]
