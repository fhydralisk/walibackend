import os
from rest_framework.views import APIView
from django.conf import settings
from django.http.response import FileResponse
from base.views import WLAPIView
from rest_framework.parsers import MultiPartParser
from ordersys.funcs.upload_photo import upload_order_photo, get_order_photo, delete_order_photo
from ordersys.serializers.photo_api import GetDeletePhotoSerializer, UploadPhotoSerializer


class UploadReceiptPhotoView(WLAPIView, APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        data, context = self.get_request_obj(request, 'GET')
        seri_api = UploadPhotoSerializer(data=data)
        self.validate_serializer(seri_api)

        photo_id = upload_order_photo(
            photo_files_form_obj=request.FILES,
            **seri_api.validated_data
        )

        return self.generate_response(data={"photo_id": photo_id}, context=context)


class DeleteReceiptPhotoView(WLAPIView, APIView):

    def get(self, request):
        data, context = self.get_request_obj(request)
        seri_api = GetDeletePhotoSerializer(data=data)
        self.validate_serializer(seri_api)

        delete_order_photo(**seri_api.data)

        return self.generate_response(data={}, context=context)


class ObtainReceiptPhotoView(WLAPIView, APIView):

    ERROR_HTTP_STATUS = True

    def get(self, request):
        data, context = self.get_request_obj(request)

        seri_api = GetDeletePhotoSerializer(data=data)
        self.validate_serializer(seri_api)

        photo_path = get_order_photo(**seri_api.data)
        real_path = os.path.join(settings.BASE_DIR, photo_path)

        return FileResponse(open(real_path), content_type='image')
