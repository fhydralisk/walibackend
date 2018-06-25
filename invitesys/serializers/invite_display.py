from rest_framework import serializers
from invitesys.models import InviteInfo
from invitesys.model_choices.invite_enum import i_status_choice
from usersys.models import UserBase
from usersys.model_choices.user_enum import role_choice
from .contract import ContractInfoSerializer


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


class InviteReadableDisplaySerializer(serializers.ModelSerializer):

    inviter = UserInfoSerializer(inviter=True, source='uid_s')
    invitee = UserInfoSerializer(inviter=False, source='uid_t')

    tname1 = serializers.ReadOnlyField(source='dmid_t.qid.t3id.t2id.t1id.tname1')
    tname2 = serializers.ReadOnlyField(source='dmid_t.qid.t3id.t2id.tname2')
    tname3 = serializers.ReadOnlyField(source='dmid_t.qid.t3id.tname3')
    pqdesc = serializers.ReadOnlyField(source='dmid_t.qid.pqdesc')
    pwcdesc = serializers.ReadOnlyField(source='dmid_t.wcid.pwcdesc')
    pmdesc = serializers.ReadOnlyField(source='pmid.opmdesc')
    disdesc = serializers.ReadOnlyField(source='disid.odmdesc')
    deposit_scale = serializers.ReadOnlyField(source='pmid.deposit_scale')
    related_order = serializers.PrimaryKeyRelatedField(source='invite_order', read_only=True)
    reason_class = serializers.SlugRelatedField(slug_field='reason', read_only=True)

    contracts = ContractInfoSerializer(source='invite_contract', many=True, read_only=True)
    invite_photo = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def to_representation(self, instance):
        # type: (InviteInfo) -> dict
        ret = super(InviteReadableDisplaySerializer, self).to_representation(instance)

        if instance.i_status == i_status_choice.INVITEE_NEGOTIATE:
            ret["invitee"]["is_negotiator"] = True
            ret["inviter"]["is_negotiator"] = False
        elif instance.i_status == i_status_choice.INVITER_NEGOTIATE:
            ret["invitee"]["is_negotiator"] = False
            ret["inviter"]["is_negotiator"] = True

        if instance.uid_s.role == role_choice.BUYER:
            ret["buyer"] = ret.pop("inviter")
            ret["seller"] = ret.pop("invitee")
        else:
            ret["buyer"] = ret.pop("invitee")
            ret["seller"] = ret.pop("inviter")

        return ret

    class Meta:
        model = InviteInfo
        fields = (
            'id',
            'inviter', 'invitee',
            'dmid_s', 'dmid_t', 'quantity', 'reason', 'reason_class',
            'price', 'unit', 'pmid', 'disid', 'dis_duration', 'i_status',
            'tname1', 'tname2', 'tname3', 'pqdesc', 'pwcdesc', 'pmdesc', 'disdesc',
            'contracts',
            'deposit_scale',
            'earnest', 'final_price', 'total_price', 'related_order',
            'invite_photo',
        )
