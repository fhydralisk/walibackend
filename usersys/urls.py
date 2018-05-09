from django.conf.urls import url, include
from usersys.views import login_views, register_views, resetpasswd_views, info_views, validate_views

register_urls = [
    url(r'^pn/pn/$', register_views.PNPostPhoneNumber.as_view()),
    url(r'^pn/validate/$', register_views.PNValidate.as_view()),
    url(r'^pn/passwd/$', register_views.PNFinalizeRegister.as_view())
]

login_urls = [
    url(r'^login/$', login_views.LoginView.as_view()),
    url(r'^logout/$', login_views.LogoutView.as_view()),
]

validate_urls = [
    url(r'^fetch_info/', validate_views.ObtainValidateInfoView.as_view()),
    url(r'^fetch_photo/', validate_views.FetchPhotoView.as_view()),
    url(r'^submit_photo/', validate_views.SubmitPhotoView.as_view()),
    url(r'^delete_photo/', validate_views.DeletePhotoView.as_view()),
    url(r'^submit_info/$', validate_views.SaveValidationInfoView.as_view()),
]

reset_passwd_urls = [
    url(r'^pn/pn/$', register_views.PNPostPhoneNumber.as_view()),
    url(r'^pn/validate/', resetpasswd_views.ResetPasswordView.as_view()),
]

info_urls = [
    url(r'^self/', info_views.UserInfoView.as_view())
]

urlpatterns = [
    url(r'^register/', include(register_urls)),
    url(r'^login/', include(login_urls)),
    url(r'^validate/', include(validate_urls)),
    url(r'^resetpasswd/', include(reset_passwd_urls)),
    url(r'^info/', include(info_urls)),
]
