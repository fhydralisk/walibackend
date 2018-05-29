from rest_framework import serializers
from ordersys.models import OrderProtocol, OrderInfo
from invitesys.serializers.invite_display import InviteReadableDetailDisplaySerializer
from paymentsys.serializers.receipt import PaymentReceiptSerializer
from .distribution import OrderLogisticsInfoSerializer
from usersys.serializers.validate_api import ValidationInfoInvoiceSerializer


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

    class Meta:
        model = OrderInfo
        fields = ('id', 'o_status', 'current_protocol', 'current_receipt', 'invite', 'logistics', 'invoice')
