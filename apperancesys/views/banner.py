import os
from rest_framework.views import APIView
from rest_framework_extensions.etag.decorators import etag
from django.conf import settings
from django.http.response import FileResponse
from base.views import WLAPIView
from apperancesys.funcs.banner import get_banner


class ObtainBannerView(WLAPIView, APIView):

    ERROR_HTTP_STATUS = True

    def dispatch(self, request, *args, **kwargs):

        self.banner_photo = get_banner()

        return super(ObtainBannerView, self).dispatch(request, *args, **kwargs)

    @etag(etag_func='get_banner_etag')
    def get(self, request):
        real_path = os.path.join(settings.BASE_DIR, self.banner_photo.image.path)

        return FileResponse(open(real_path), content_type='image')

    def get_banner_etag(self, view_instance, view_method,request, args, kwargs):

        return '"%d"' % self.banner_photo.id
