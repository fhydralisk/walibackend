from django.conf.urls import include, url
import views.obtain as obtain
import views.operate as operate


url_pattern_obtain = [
    url(r'^defaultinvite/', obtain.ObtainDefaultInviteView.as_view()),
    url(r'^selfinvite/', obtain.ObtainInvite2SelfAppraisalView.as_view()),
    url(r'^invitedetail/', obtain.ObtainInvite2AppraisalSDetailView.as_view()),
]

url_pattern_operate = [
    url(r'^submitinvite/', operate.SubmitInviteView.as_view()),
    url(r'^cancelinvite/', operate.CancelInviteView.as_view()),
]


url_pattern = [
    url(r'^obtain/', include(url_pattern_obtain)),
    url(r'^operate/', include(url_pattern_operate)),
]
