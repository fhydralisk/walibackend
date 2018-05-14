from django.conf.urls import url, include
from views.invite import ObtainInviteView, ObtainInviteDetailView, PublishInviteView, FlowHandleView
from views.contract import RetrieveContractInfoView, ObtainContractContentView, SignContractView


obtain_urlpatterns = [
    url(r'^self/', ObtainInviteView.as_view()),
    url(r'^detail/', ObtainInviteDetailView.as_view()),
]

launch_urlpatterns = [
    url(r'^launch/$', PublishInviteView.as_view()),
]

flow_urlpatterns = [
    url(r'^handle/$', FlowHandleView.as_view()),
]

contract_urlpatterns = [
    url(r'^info/', RetrieveContractInfoView.as_view()),
    url(r'^content/', ObtainContractContentView.as_view()),
    url(r'^sign/$', SignContractView.as_view()),
]

urlpatterns = [
    url(r'^flow/', include(flow_urlpatterns)),
    url(r'^obtain/', include(obtain_urlpatterns)),
    url(r'^launch/', include(launch_urlpatterns)),
    url(r'contract/', include(contract_urlpatterns)),
]
