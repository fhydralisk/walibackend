import os

from django.conf import settings
from django.http.response import FileResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from base.views import WLAPIView
from usersys.funcs.validate import get_validate_photo, submit_validate_photo, \
    get_validate, save_validate, delete_validate_photo
from usersys.serializers.validate_api import \
    ValidationPhotoSerializer, ValidationSubmitSerializer, ValidationInfoDisplaySeralizer
from usersys.funcs.placeholder2exceptions import get_placeholder2exception


class FetchPhotoView(WLAPIView, APIView):

    ERROR_HTTP_STATUS = True

    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ValidationPhotoSerializer(data=data)
        self.validate_serializer(seri)

        photo_path = get_validate_photo(**seri.data)
        real_path = os.path.join(settings.BASE_DIR, photo_path)

        return FileResponse(open(real_path), content_type='image')


class SubmitPhotoView(WLAPIView, APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request):
        data, context = self.get_request_obj(request, 'GET')
        try:
            photo_id = submit_validate_photo(
                user_sid=data["user_sid"],
                t_photo=data["t_photo"],
                photo_files_form_obj=request.FILES
            )
        except KeyError:
            raise get_placeholder2exception("user/validate/submit_photo/ : bad request")

        else:
            return self.generate_response(data={"photo_id": photo_id}, context=context)


class DeletePhotoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = ValidationPhotoSerializer(data=data)
        self.validate_serializer(seri)

        delete_validate_photo(**seri.data)

        return self.generate_response(data={}, context=context)


class SaveValidationInfoView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)

        seri = ValidationSubmitSerializer(data=data)
        self.validate_serializer(seri)

        # use validated_data in case user dose not finish some of the fields.
        # print seri.fields.items()
        # print seri.data

        save_validate(**seri.data)
        return self.generate_response(data={}, context=context)


class ObtainValidateInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        try:
            validate, areas, photos = get_validate(user_sid=data["user_sid"])
            seri_return = ValidationInfoDisplaySeralizer(instance={
                "validate_obj": validate,
                "validate_areas": areas,
                "validate_photos_uploaded": photos
            })
            return self.generate_response(data=seri_return.data, context=context)
        except KeyError:
            raise get_placeholder2exception("user/validate/fetch_info/ : bad request")
