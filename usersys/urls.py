from django.conf.urls import url,include
import register_views

register_urls = [
    url(r'^pn/pn/$', register_views.PNPostPhoneNumber.as_view()),
    url(r'^pn/validate/$', register_views.PNValidate.as_view()),
    url(r'^pn/passwd/$', register_views.PNFinalizeRegister.as_view())
]

urlpatterns = [
    url(r'^register/', include(register_urls)),
    #url('^')
]
