import os
from django.conf import settings
from django.http.response import FileResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from base.views import WLAPIView
from appraisalsys.serializers.photo_api import (
    UploadCheckPhotoSerializer, GetDeleteCheckPhotoSerializer
)
from appraisalsys.funcs.photo import upload_check_photo, delete_check_photo, get_check_photo

class UploadCheckPhotoView(WLAPIView, APIView):
    parser_classes = (MultiPartParser,)

    def post(self, requset):
        data, context = self.get_request_obj(requset, 'GET')
        seri_api = UploadCheckPhotoSerializer(data=data)
        self.validate_serializer(seri_api)

        photo_id = upload_check_photo(
            photo_files_from_obj=requset.FILES,
            **seri_api.validated_data
        )
        return self.generate_response(
            data={
                "photo_id": photo_id
            },
            context=context
        )

class DeleteCheckPhotoView(WLAPIView, APIView):

    def get(self, request):
        data, context = self.get_request_obj(request)
        seri_api = GetDeleteCheckPhotoSerializer(data=data)
        self.validate_serializer(seri_api)

        delete_check_photo(**seri_api.data)

        return self.generate_response(data={}, context=context)


class ObtainCheckPhotoView(WLAPIView, APIView):

    ERROR_HTTP_STATUS = True

    def get(self, reuest):
        data, context = self.get_request_obj(reuest)

        seri_api = GetDeleteCheckPhotoSerializer(data=data)
        self.validate_serializer(seri_api)

        photo_path = get_check_photo(**seri_api.data)
        real_path = os.path.join(settings.BASE_DIR, photo_path)

        return FileResponse(open(real_path), content_type='image')