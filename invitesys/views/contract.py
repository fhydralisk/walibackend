from rest_framework.views import APIView
from django.http.response import HttpResponse
from base.views import WLAPIView
from invitesys.serializers.contract_api import ObtainContractInfoSerializer, SignContractSerializer
from invitesys.serializers.contract import ContractInfoSerializer
from invitesys.funcs.contracts import obtain_contract_content, retrieve_contract_info, sign_contract


class RetrieveContractInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainContractInfoSerializer(data=data)
        self.validate_serializer(seri)

        contract = retrieve_contract_info(**seri.data)

        seri_contract = ContractInfoSerializer(instance=contract)

        return self.generate_response(data={"contract_info": seri_contract.data}, context=context)


class ObtainContractContentView(WLAPIView, APIView):
    ERROR_HTTP_STATUS = True

    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ObtainContractInfoSerializer(data=data)
        self.validate_serializer(seri)

        content = obtain_contract_content(**seri.data)

        return HttpResponse(content)


class SignContractView(WLAPIView, APIView):

    def post(self, request):
        data, context = self.get_request_obj(request)

        seri = SignContractSerializer(data=data)
        self.validate_serializer(seri)

        contract = sign_contract(**seri.data)

        seri_contract = ContractInfoSerializer(instance=contract)

        return self.generate_response(data={"contract_info": seri_contract.data}, context=context)
