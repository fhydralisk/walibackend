import logging
from rest_framework import serializers
from simplified_invite.models import InviteInfo
from simplified_invite.model_choices.invite_enum import i_status_choice
from demandsys.serializers.validators.address_submit import AddressChoiceValidator
from usersys.models import UserBase
from appraisalsys.serializers.appraisal import AppraisalInfoDisplaySerializer
from appraisalsys.models.appraise import AppraisalInfo
from demandsys.serializers.demand import DemandPhotoSerializers


logger = logging.getLogger(__name__)


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

    def to_representation(self, instance):
        # type: (InviteInfo) -> dict

        data = super(InviteInfoDisplaySerializer, self).to_representation(instance)
        if instance.i_status == i_status_choice.SIGNED:
            try:
                appr_obj = instance.appraisal
                data['price'] = appr_obj.final_price
                data['quantity'] = appr_obj.net_weight - appr_obj.tare if appr_obj.tare is not None \
                    else appr_obj.net_weight * (1 - appr_obj.deduction_ratio/100) if appr_obj.deduction_ratio is not None \
                    else appr_obj.net_weight
                data['total_price'] = data['price'] * data['quantity']
            except AppraisalInfo.DoesNotExist:
                logger.warning("This invite's status is signed but it has no appraisal")

        return data


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
