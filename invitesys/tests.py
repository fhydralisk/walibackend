from django.test import TestCase

from usersys.models import UserBase, UserValidate
from usersys.models.user_enum import role_choice
from coresys.models import CoreDistributionMethod, CorePaymentMethod
from demandsys.models import ProductDemand, ProductTypeL1, ProductTypeL2, ProductTypeL3, ProductQuality, ProductWaterContent
from invitesys.models import InviteInfo
from serializers.invite_display import UserInfoSerializer, InviteReadableDisplaySerializer

from serializers.invite_api import PublishInviteSerializer
from serializers.invite import InviteInfoSubmitSerializer

def create_user():
    user = UserBase.objects.create_user('18513958704', '123456', role=role_choice.BUYER)
    UserValidate.objects.create(uid=user, t_user=1, validate_status=1)
    user = UserBase.objects.create_user('18513938705', '123456', role=role_choice.SELLER)
    UserValidate.objects.create(uid=user, t_user=1, validate_status=1)


def create_pt():
    t1 = ProductTypeL1.objects.create(
        tname1="Test1"
    )
    t2 = ProductTypeL2.objects.create(
        tname2="Test2",
        t1id=t1
    )
    t3 = ProductTypeL3.objects.create(
        tname3="Test3",
        t2id=t2
    )
    ProductQuality.objects.create(
        pqdesc="TestQ",
        ord=1,
        t3id=t3
    )
    ProductWaterContent.objects.create(
        pwcdesc="TestWC",
        ord=1,
    )


def create_demand():
    ProductDemand.objects.create(
        uid_id=1,
        t_demand=1,
        pid_id=1,
        qid_id=1,
        wcid_id=1,
        quantity=10,
        min_quantity=1,
        price=100,
        unit=1,
        pmid_id=1,
        duration=1,
        description="Test",
        comment="Test",
    )


def create_pm():
    CorePaymentMethod.objects.create(ord=1, deposit_scale=0.1, opmdesc="Test", in_use=True)


def create_dm():
    CoreDistributionMethod.objects.create(odmdesc="TestDM")


def create_invite():
    seller = UserBase.objects.filter(role=role_choice.SELLER).first()
    buyer = UserBase.objects.filter(role=role_choice.BUYER).first()
    InviteInfo.objects.create(
        uid_s=seller,
        uid_t=buyer,
        dmid_t_id=1,
        quantity=10,
        price=10,
        pmid_id=1,
        disid_id=1,
        dis_duration=10,
        i_status=0,
        unit=1,
    )


# Create your tests here.
class UserInfoSerializerTest(TestCase):

    def setUp(self):
        create_user()
        create_pt()
        create_pm()
        create_dm()
        create_demand()
        create_invite()

    # def test_user_info_return(self):
    #     u = UserBase.objects.get(id=2)
    #     uis = UserInfoSerializer(instance=u, inviter=True)
    #     irds = InviteReadableDisplaySerializer(instance=InviteInfo.objects.first())
    #     print uis.data
    #     print irds.data

    def test_invite_submit_serializer(self):
        data = {
            "user_sid": "1a2b3c4d5e6f7g890",
            "invite": {
                "dmid_s": None,
                "dmid_t": 1,
                "quantity": 5.0,
                "price": 2600,
                "unit": 1,
                "pmid": 1,
                "dis_duration": 10
            }
        }

        publish_seri = PublishInviteSerializer(data=data)
        self.assertTrue(publish_seri.is_valid())
        submit_seri = InviteInfoSubmitSerializer(data=publish_seri.data["invite"])
        self.assertTrue(submit_seri.is_valid())

