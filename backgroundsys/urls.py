from django.contrib import admin
from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^',admin.site.urls),
    url(r'^choose/province/', views.choose_province),
]
