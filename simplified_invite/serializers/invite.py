from rest_framework import serializers
from simplified_invite.models import InviteInfo
from demandsys.serializers.validators.address_submit import AddressChoiceValidator
from usersys.models import UserBase
from appraisalsys.serializers.appraisal import AppraisalInfoDisplaySerializer
from demandsys.serializers.demand import DemandPhotoSerializers


class DefaultInviterInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = InviteInfo
        fields = ("price", "quantity", "aid", "street",)


class UserInfoSerializer(serializers.ModelSerializer):

    def __init__(self, inviter, *args, **kwargs):
        self.inviter = inviter
        super(UserInfoSerializer, self).__init__(*args, **kwargs)

    validate_contact = serializers.ReadOnlyField(source='user_validate.contact')
    validate_company = serializers.ReadOnlyField(source='user_validate.company')
    validate_t_user = serializers.ReadOnlyField(source='user_validate.t_user')
    is_inviter = serializers.SerializerMethodField()

    class Meta:
        model = UserBase
        fields = (
            'id', 'pn', 'role',
            'validate_contact', 'validate_company', 'validate_t_user',
            'is_inviter'
        )

    def get_is_inviter(self, obj):
        if self.inviter:
            return 1
        else:
            return 0


class InviteInfoDisplaySerializer(serializers.ModelSerializer):

    buyer = UserInfoSerializer(inviter=True, source='uid_s')
    seller = UserInfoSerializer(inviter=False, source='uid_t')

    tname1 = serializers.ReadOnlyField(source='dmid_t.pid.t2id.t1id.tname1')
    tname2 = serializers.ReadOnlyField(source='dmid_t.pid.t2id.tname2')
    tname3 = serializers.ReadOnlyField(source='dmid_t.pid.tname3')
    pwcdesc = serializers.ReadOnlyField(source='dmid_t.wcid.pwcdesc')
    related_appraisal = AppraisalInfoDisplaySerializer(source='appraisal')
    reason_class = serializers.SlugRelatedField(slug_field='reason', read_only=True)
    demand_photos = DemandPhotoSerializers(read_only=True, many=True, source='dmid_t.demand_photo')
    demand_photo_ids = serializers.PrimaryKeyRelatedField(read_only=True, many=True, source='dmid_t.demand_photo')

    class Meta:
        model = InviteInfo
        fields = (
            'id',
            'buyer', 'seller', 'aid', 'street',
            'dmid_s', 'dmid_t', 'quantity', 'reason', 'reason_class',
            'demand_photos', 'demand_photo_ids',
            'price', 'i_status',
            'tname1', 'tname2', 'tname3', 'pwcdesc',
            'total_price', 'related_appraisal',
        )


class SelfInviteDisplaySerializer(InviteInfoDisplaySerializer):

    class Meta:
        model = InviteInfo
        fields = InviteInfoDisplaySerializer.Meta.fields


class InviteDetailDisplaySerializer(InviteInfoDisplaySerializer):

    template_id = serializers.SlugRelatedField(
        slug_field='template_id',
        source='dmid_t.pid.t2id.t1id.json_schema_of_appraisal.last',
        read_only=True
    )
    class Meta:
        model = InviteInfo
        fields = InviteInfoDisplaySerializer.Meta.fields + ("template_id",)


class InviteInfoInAppraisalSysSubmitSerializer(serializers.ModelSerializer):

    class Meta:
        model = InviteInfo
        fields = (
            'dmid_t',
            'quantity',
            'price',
            'aid',
            'street',
            'abid',
        )
        validators = [
            AddressChoiceValidator()
        ]
