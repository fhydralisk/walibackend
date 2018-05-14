"""walibackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
import usersys.urls
import coresys.urls
import invitesys.urls

urlpatterns = [
    url(r'^bg/', admin.site.urls),
    url(r'^core/', include(coresys.urls.urlpatterns)),
    url(r'^user/', include(usersys.urls.urlpatterns)),
    # url(r'^demand/', include('demandsys.urls')),
    url(r'^invite/', include(invitesys.urls.urlpatterns)),
    # url(r'^order/', include('ordersys.urls')),
    # url(r'^payment/', include('paymentsys.urls')),

]
