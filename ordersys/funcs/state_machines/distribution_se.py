from base.util.db import update_instance_from_dict
from base.exceptions import WLException
from base.util.serializer_helper import errors_summery
from ordersys.models import OrderLogisticsInfo, OrderInfo
from ordersys.serializers.distribution import OrderLogisticsInfoSubmitSerializer
from ordersys.model_choices.photo_enum import photo_type_choice


def append_order_logistics_info(ctx, extra_ctx, **kwargs):
    """

    :param ctx:
    :param extra_ctx:
    :param kwargs:
    :return:
    """

    l_type = ctx["l_type"]
    parameter = extra_ctx["parameter"]
    order = extra_ctx["order"]  # type: OrderInfo
    dmseri = OrderLogisticsInfoSubmitSerializer(data=parameter["loginfo"])
    if not dmseri.is_valid():
        raise WLException(400, errors_summery(dmseri))

    try:
        logistics = OrderLogisticsInfo.objects.get(oid=order, l_type=l_type)
        update_instance_from_dict(logistics, dmseri.validated_data, False)
    except OrderLogisticsInfo.DoesNotExist:
        logistics = OrderLogisticsInfo(**dmseri.validated_data)
        logistics.oid = order
        logistics.l_type = ctx["l_type"]

    logistics.save()


def check_order_receipt_photo(ctx, extra_ctx, **kwargs):
    """

    :param ctx:
    :param extra_ctx:
    :param kwargs:
    :return:
    """

    chk_type = ctx["chk_type"]
    assert(chk_type in photo_type_choice.get_choices())

    order = extra_ctx["order"]  # type: OrderInfo
    if not order.order_receipt_photos.filter(in_use=True, photo_type=chk_type).exists():
        raise WLException(403, "Please upload photos.")
