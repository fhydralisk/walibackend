import os
from rest_framework.views import APIView
from rest_framework_extensions.etag.decorators import etag
from django.conf import settings
from django.http.response import FileResponse
from base.views import WLAPIView
from apperancesys.funcs.banner import get_banner
from apperancesys.funcs.placeholder2exceptions import get_placeholder2exception


class ObtainBannerView(WLAPIView, APIView):

    ERROR_HTTP_STATUS = True

    def dispatch(self, request, *args, **kwargs):

        self.banner_photos = get_banner(3)

        return super(ObtainBannerView, self).dispatch(request, *args, **kwargs)

    @etag(etag_func='get_banner_etag')
    def get(self, request, seq):
        real_path = os.path.join(settings.BASE_DIR, self.banner_photos[int(seq)-1].image.path)

        return FileResponse(open(real_path), content_type='image')

    def get_banner_etag(self, view_instance, view_method,request, args, kwargs):
        seq = int(kwargs["seq"]) - 1
        try:
            return '"%d"' % self.banner_photos[seq].id
        except IndexError:
            raise get_placeholder2exception("appearance/banner/ : no banner in  get_banner_etag")
