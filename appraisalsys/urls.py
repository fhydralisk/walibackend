from django.conf.urls import include, url
import views.operate as operate


url_pattern_operate = [
    url(r'^submitappraisal/', operate.SubmitAppraisalView.as_view()),
]


url_pattern = [
    url(r'^operate/', include(url_pattern_operate)),
]
