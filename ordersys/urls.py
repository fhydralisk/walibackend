from django.conf.urls import include, url
import views.obtain as obtain
import views.operate as operate

url_pattern_obtain = [
    url(r'^list/', obtain.ObtainOrderView.as_view()),
    url(r'^order/', obtain.ObtainOrderDetailView.as_view()),
]


url_pattern_operate = [
    url(r'^order/$', operate.OperateOrderView.as_view()),
    url(r'^protocol/$', operate.OperateProtocolView.as_view()),
]


url_pattern = [
    url(r'^info/', include(url_pattern_obtain)),
    url(r'^operate/', include(url_pattern_operate)),
]
