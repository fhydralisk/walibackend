from django.conf.urls import include, url
import views.obtain as obtain
import views.operate as operate
import views.photo as photo

url_pattern_obtain = [
    url(r'^list/', obtain.ObtainOrderView.as_view()),
    url(r'^order/', obtain.ObtainOrderDetailView.as_view()),
]


url_pattern_operate = [
    url(r'^order/$', operate.OperateOrderView.as_view()),
    url(r'^protocol/$', operate.OperateProtocolView.as_view()),
]


url_pattern_photo = [
    url(r'^upload/', photo.UploadReceiptPhotoView.as_view()),
    url(r'^delete/', photo.DeleteReceiptPhotoView.as_view()),
    url(r'^obtain/', photo.ObtainReceiptPhotoView.as_view()),
]


url_pattern = [
    url(r'^info/', include(url_pattern_obtain)),
    url(r'^operate/', include(url_pattern_operate)),
    url(r'^photo/', include(url_pattern_photo)),
]
