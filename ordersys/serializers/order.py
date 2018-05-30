from rest_framework import serializers
from usersys.serializers.validate_api import ValidationInfoInvoiceSerializer
from invitesys.models import InviteInfo
from invitesys.serializers.invite_display import InviteReadableDetailDisplaySerializer
from ordersys.models import OrderProtocol, OrderInfo
from paymentsys.serializers.receipt import PaymentReceiptSerializer
from .distribution import OrderLogisticsInfoSerializer


class BuyerAddressSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField(source='buyer.user_validate.contact')
    phone = serializers.ReadOnlyField(source='buyer.pn')
    province = serializers.ReadOnlyField(source='aid.cid.pid.province')
    city = serializers.ReadOnlyField(source='aid.cid.city')
    area = serializers.ReadOnlyField(source='aid.area')

    class Meta:
        model = InviteInfo
        fields = ('name', 'phone', 'province', 'city', 'area', 'street')


class OrderProtocolSubmitSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProtocol
        fields = ('op_type', 'c_price', "description")


class OrderProtocolDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProtocol
        fields = '__all__'


class OrderInfoDisplaySerializer(serializers.ModelSerializer):
    current_protocol = OrderProtocolDisplaySerializer(read_only=True)
    current_receipt = PaymentReceiptSerializer(read_only=True)
    invite = InviteReadableDetailDisplaySerializer(source='ivid', read_only=True)
    logistics = OrderLogisticsInfoSerializer(source='order_logistics', read_only=True, many=True)
    invoice = ValidationInfoInvoiceSerializer(source='buyer_invoice_info', read_only=True)
    buyer_address = BuyerAddressSerializer(source='ivid')

    class Meta:
        model = OrderInfo
        fields = (
            'id', 'o_status', 'current_protocol', 'current_receipt',
            'invite', 'logistics', 'invoice', 'buyer_address',
        )
