from django.conf.urls import url, include
from usersys.views import login, register, resetpasswd, info, validate

register_urls = [
    url(r'^pn/pn/$', register.PNPostPhoneNumber.as_view()),
    url(r'^pn/validate/$', register.PNValidate.as_view()),
    url(r'^pn/passwd/$', register.PNFinalizeRegister.as_view())
]

login_urls = [
    url(r'^login/$', login.LoginView.as_view()),
    url(r'^logout/$', login.LogoutView.as_view()),
]

validate_urls = [
    url(r'^fetch_info/', validate.ObtainValidateInfoView.as_view()),
    url(r'^fetch_photo/', validate.FetchPhotoView.as_view()),
    url(r'^submit_photo/', validate.SubmitPhotoView.as_view()),
    url(r'^delete_photo/', validate.DeletePhotoView.as_view()),
    url(r'^submit_info/$', validate.SaveValidationInfoView.as_view()),
]

reset_passwd_urls = [
    url(r'^pn/pn/$', register.PNPostPhoneNumber.as_view()),
    url(r'^pn/validate/$', resetpasswd.ResetPasswordView.as_view()),
    url(r'^changepasswd/$', resetpasswd.ChangePasswordView.as_view()),
]

info_urls = [
    url(r'^self/', info.UserInfoView.as_view()),
    url(r'^getsearchhistory/', info.GetSearchHistoryView.as_view()),
    url(r'^emptysearchhistory', info.EmptySearchHistoryView.as_view()),
]

urlpatterns = [
    url(r'^register/', include(register_urls)),
    url(r'^login/', include(login_urls)),
    url(r'^validate/', include(validate_urls)),
    url(r'^resetpasswd/', include(reset_passwd_urls)),
    url(r'^info/', include(info_urls)),
]
