import xlwt
import io
from rest_framework import serializers
from django.utils.timezone import now
from django.http.response import FileResponse
from logsys.models import LogOrderProtocolStatus, LogOrderStatus
from invitesys.models import InviteInfo
from usersys.serializers.user_info import UserInfoSerialzier


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteInfo
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(InviteSerializer, self).to_representation(instance)
        # uid_s = rep.pop('uid_s')
        # uid_t = rep.pop('uid_t')
        # for k, v in uid_s.items():
        #     rep['uid_s_%s' % k] = v
        # for k, v in uid_t.items():
        #     rep['uid_t_%s' % k] = v

        return rep


class LogOrderSerializer(serializers.ModelSerializer):
    invite = InviteSerializer(read_only=True, source='oid.ivid')
    final_price = serializers.ReadOnlyField(source='oid.final_price')

    class Meta:
        model = LogOrderStatus
        fields = (
            'log_date_time',
            'oid',
            'o_status',
            'context',
            'final_price',
            'operator',
            'invite',
        )

    def to_representation(self, instance):
        rep = super(LogOrderSerializer, self).to_representation(instance)
        invite = rep.pop('invite')
        for k, v in invite.items():
            rep['invite_%s' % k] = v

        return rep


class LogOrderProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogOrderProtocolStatus
        fields = (
            'log_date_time',
            'operator',
            'opid',
            'p_status',
            'p_operate_status',
            'context',
        )


def xls(data):
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('order')
    try:
        for i, h in enumerate(data[0].keys()):
            sheet.write(0, i, h)
    except IndexError:
        return

    for row, r in enumerate(data):
        for col, d in enumerate(r.values()):
            sheet.write(row + 1, col, d)

    f = io.BytesIO()
    wb.save(f)
    f.seek(0)
    return f


def fetch_order_log():
    order_logs = LogOrderStatus.objects.all()
    seri = LogOrderSerializer(order_logs, many=True)
    serialized_data = seri.data

    # convert to excel
    f = xls(serialized_data)
    return f


def order_log_view(request, **kwargs):
    f = fetch_order_log()
    r = FileResponse(f, content_type='application/x-xls')
    r['Content-Disposition'] = 'inline; filename=order-{date}.xls'.format(
        date=now()
    )
    return r