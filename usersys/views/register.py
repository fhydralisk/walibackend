from rest_framework.views import APIView

from base.views import WLAPIView
from usersys.serializers.register_api import PNSubmitSerializer, PNValidateSerializer, PNFinalRegisterSerializer
from usersys.funcs.registration import get_sid_by_phonenumber, validate_sid, register

# Create your views here.


class PNPostPhoneNumber(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        pnseri = PNSubmitSerializer(data=data)
        # FIXME: If user already registered, it will throw an exception.
        self.validate_serializer(pnseri)

        sid = get_sid_by_phonenumber(pnseri.data["pn"])
        return self.generate_response(data={
            "pn": pnseri.data["pn"],
            "sid": sid
        }, context=context)


class PNValidate(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        pnseri = PNValidateSerializer(data=data)
        self.validate_serializer(pnseri)

        validate_sid(**pnseri.data)
        return self.generate_response(data={
            "pn": pnseri.data["pn"],
            "sid": pnseri.data["sid"]
        }, context=context)


class PNFinalizeRegister(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        ser_reg = PNFinalRegisterSerializer(data=data)
        self.validate_serializer(ser_reg)

        register(**ser_reg.data)

        return self.generate_response(data={
            "pn": ser_reg.data["pn"]
        }, context=context)
