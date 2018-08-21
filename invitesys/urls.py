from django.conf.urls import url, include
from views.invite import (
    ObtainInviteView, ObtainInviteDetailView, PublishInviteView,
    FlowHandleView, ObtainInviteCancelReasonClassView
)
from views.photo import DeleteInvitePhotoView, ObtainInvitePhotoView, UploadInvitePhotoView


obtain_urlpatterns = [
    url(r'^self/', ObtainInviteView.as_view()),
    url(r'^detail/', ObtainInviteDetailView.as_view()),
    url(r'^cancel_reason/$', ObtainInviteCancelReasonClassView.as_view()),
]

launch_urlpatterns = [
    url(r'^launch/$', PublishInviteView.as_view()),
]

flow_urlpatterns = [
    url(r'^handle/$', FlowHandleView.as_view()),
]


photo_urlpatterns = [
    url(r'^upload/', UploadInvitePhotoView.as_view()),
    url(r'^obtain/', ObtainInvitePhotoView.as_view()),
    url(r'^delete/', DeleteInvitePhotoView.as_view()),
]

urlpatterns = [
    url(r'^flow/', include(flow_urlpatterns)),
    url(r'^obtain/', include(obtain_urlpatterns)),
    url(r'^launch/', include(launch_urlpatterns)),
    url(r'^photo/', include(photo_urlpatterns)),
]
