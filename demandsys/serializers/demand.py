from rest_framework import serializers
from demandsys.models import ProductDemand, ProductDemandPhoto


class DemandPhotoSerializers(serializers.ModelSerializer):

    upload_date = serializers.SerializerMethodField()

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
            'id', 't_demand', 'price', 'quantity', 'min_quantity', 'unit', 'match',
            'company', 'contact', 't_user',
            'tname1', 'tname2', 'tname3', 'pqdesc', 'pwcdesc', 'pmdesc',
            'area', 'city', 'province',
            'satisfied',
            'demand_photos', 'demand_photo_ids'
        )

    def get_satisfied(self, obj):
        return obj.quantity - obj.quantity_left()


class DemandPublishSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDemand
        exclude = (
            'id', 't_demand', 'st_time', 'uid', 'in_use', 'create_datetime',
        )


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
        exclude = (
            'id', 't_demand', 'st_time', 'uid', 'in_use', 'create_datetime', 'pid', 'wcid',
        )
