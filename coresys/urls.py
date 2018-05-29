from django.conf.urls import url, include
from coresys.views.address import GetAreaView, GetCityView, GetProvinceView, GetAllFView
from coresys.views.info import CoreInfoPDView

address_urlpatterns = [
    url(r'^province/', GetProvinceView.as_view()),
    url(r'^city/', GetCityView.as_view()),
    url(r'^area/', GetAreaView.as_view()),
    url(r'^fdict/', GetAllFView.as_view()),
]

info_urlpatterns = [
    url(r'^pd/', CoreInfoPDView.as_view()),
]

urlpatterns = [
    url(r'^address/', include(address_urlpatterns)),
    url(r'^info/', include(info_urlpatterns)),
]
