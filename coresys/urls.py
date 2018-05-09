from django.conf.urls import url, include
from coresys.views.address import GetAreaView, GetCityView, GetProvinceView

address_urlpatterns = [
    url(r'^province/', GetProvinceView.as_view()),
    url(r'^city/', GetCityView.as_view()),
    url(r'^area/', GetAreaView.as_view()),
]


urlpatterns = [
    url(r'^address/', include(address_urlpatterns)),
]
