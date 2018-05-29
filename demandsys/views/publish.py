from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from base.views import WLAPIView
from demandsys.serializers.demand_api import PublishDemandSerializer, EditDemandSerializer, CloseDeleteDemandSerializer
from demandsys.serializers.photo_api import UploadPhotoSerializer, RemovePhotoSerializer
from demandsys.funcs.issue import publish_demand, edit_demand, upload_photo, shut_demand, delete_photo, delete_demand


class PublishDemandView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)

        seri = PublishDemandSerializer(data=data)
        self.validate_serializer(seri)

        dmid = publish_demand(**seri.validated_data)

        return self.generate_response(data={"dmid": dmid}, context=context)


class EditDemandView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)

        seri = EditDemandSerializer(data=data, partial=True)
        self.validate_serializer(seri)

        dmid = edit_demand(**seri.validated_data)

        return self.generate_response(data={"dmid": dmid}, context=context)


class ShutDemandView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = CloseDeleteDemandSerializer(data=data)
        self.validate_serializer(seri)

        shut_demand(**seri.data)

        return self.generate_response(data={}, context=context)


class DeleteDemandView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = CloseDeleteDemandSerializer(data=data)
        self.validate_serializer(seri)

        delete_demand(**seri.data)

        return self.generate_response(data={}, context=context)


class UploadPhotoView(WLAPIView, APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request):
        data, context = self.get_request_obj(request, 'GET')
        seri = UploadPhotoSerializer(data=data)
        self.validate_serializer(seri)

        photo_id = upload_photo(photo_from_object=request.FILES, **seri.data)

        return self.generate_response(data={"photo_id": photo_id}, context=context)


class RemovePhotoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = RemovePhotoSerializer(data=data)
        self.validate_serializer(seri)

        delete_photo(**seri.data)

        return self.generate_response(data={}, context=context)
