from django.conf.urls import url, include
from demandsys.views.obtain import ObtainHotView, ObtainSelfView, ObtainDetailView, ObtainPhotoDataView, ObtainMatchView
from demandsys.views.catalog import GetTreedProductTypeView, GetFTreedProductTypeView, GetProductTypeL1
from demandsys.views.publish import (
    EditDemandView, PublishDemandView, RemovePhotoView, ShutDemandView, UploadPhotoView, DeleteDemandView,
)

obtain_urlpatterns = [
    url(r'^hot/', ObtainHotView.as_view()),
    url(r'^self/', ObtainSelfView.as_view()),
    url(r'^demand/', ObtainDetailView.as_view()),
    url(r'^photo/', ObtainPhotoDataView.as_view()),
    url(r'^match/', ObtainMatchView.as_view()),

]
catalog_urlpatterns = [
    url(r'^lall/', GetTreedProductTypeView.as_view()),
    url(r'^flall/', GetFTreedProductTypeView.as_view()),
    url(r'^l1/$', GetProductTypeL1.as_view()),
]

publish_urlpatterns = [
    url(r'^submit_photo/', UploadPhotoView.as_view()),
    url(r'^remove_photo/', RemovePhotoView.as_view()),
    url(r'^publish_demand/', PublishDemandView.as_view()),
    url(r'^edit_demand/', EditDemandView.as_view()),
    url(r'^close_demand/', ShutDemandView.as_view()),
    url(r'^remove_demand/', DeleteDemandView.as_view()),
]

urlpatterns = [
    url(r'^obtain/', include(obtain_urlpatterns)),
    url(r'^catalog/', include(catalog_urlpatterns)),
    url(r'^publish/', include(publish_urlpatterns)),
]
