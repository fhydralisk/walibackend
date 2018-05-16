from django.conf.urls import url, include
from demandsys.views.obtain import ObtainHotView, ObtainSelfView, ObtainDetailView
from demandsys.views.catalog import GetTreedProductTypeView

obtain_urlpatterns = [
    url(r'^hot/', ObtainHotView.as_view()),
    url(r'^self/', ObtainSelfView.as_view()),
    url(r'^demand/', ObtainDetailView.as_view()),

]
catalog_urlpatterns = [
    url(r'^lall/', GetTreedProductTypeView.as_view()),
]

publish_urlpatterns = []

urlpatterns = [
    url(r'^obtain/', include(obtain_urlpatterns)),
    url(r'^catalog/', include(catalog_urlpatterns)),
    url(r'^publish/', include(publish_urlpatterns)),
]
