from django.conf.urls import include, url
from .views import banner


url_banner_patterns = [
    url(r'^banner.jpg$', banner.ObtainBannerView.as_view()),
]


url_patterns = [
    url(r'^banner/', include(url_banner_patterns)),
]
