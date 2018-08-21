from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from invitesys.models import InviteInfo
from invitesys.serializers.invite_display import InviteReadableDisplaySerializer
from ordersys.models import OrderProtocol, OrderInfo, OrderReceiptPhoto
from ordersys.model_choices.order_enum import op_type_choice
from ordersys.model_choices.photo_enum import photo_type_choice
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

    c_price = serializers.FloatField(min_value=0.01, required=False)

    class Meta:
        model = OrderProtocol
        fields = ('op_type', 'c_price', "description")

    def validate(self, attrs):
        if attrs['op_type'] == op_type_choice.ADJUST_PRICE:
            if 'c_price' not in attrs:
                raise ValidationError({
                    u'c_price': ["This field is required."]
                }, code=400)

        return attrs


class OrderProtocolDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProtocol
        fields = '__all__'


class OrderInfoDisplaySerializer(serializers.ModelSerializer):
    current_protocol = OrderProtocolDisplaySerializer(read_only=True)
    current_receipt = PaymentReceiptSerializer(read_only=True)
    invite = InviteReadableDisplaySerializer(source='ivid', read_only=True)
    logistics = OrderLogisticsInfoSerializer(source='order_logistics', read_only=True, many=True)
    buyer_address = BuyerAddressSerializer(source='ivid')
    photo_forward = serializers.PrimaryKeyRelatedField(
        source='order_receipt_photos',
        queryset=OrderReceiptPhoto.objects.filter(photo_type=photo_type_choice.RECEIPT_FORWARD),
        many=True
    )
    photo_product = serializers.PrimaryKeyRelatedField(
        source='order_receipt_photos',
        queryset=OrderReceiptPhoto.objects.filter(photo_type=photo_type_choice.PHOTO_PRODUCTS),
        many=True
    )
    photo_check = serializers.PrimaryKeyRelatedField(
        source='order_receipt_photos',
        queryset=OrderReceiptPhoto.objects.filter(photo_type=photo_type_choice.RECEIPT_CHECK),
        many=True
    )

    class Meta:
        model = OrderInfo
        fields = (
            'id', 'o_status', 'current_protocol', 'current_receipt',
            'invite', 'logistics', 'buyer_address', 'photo_forward', 'photo_product', 'photo_check',
        )
