from django.conf.urls import include, url
import views.operate as operate
import views.photo as photo


url_pattern_operate = [
    url(r'^submitappraisal/', operate.SubmitAppraisalView.as_view()),
]

url_pattern_photo = [
    url(r'^upload/', photo.UploadCheckPhotoView.as_view()),
    url(r'^delete/', photo.DeleteCheckPhotoView.as_view()),
    url(r'^obtain/', photo.ObtainCheckPhotoView.as_view())
]


url_pattern = [
    url(r'^operate/', include(url_pattern_operate)),
    url(r'^photo/', include(url_pattern_photo)),
]
