"""DSPProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from message import views
# from message.views import getform,getHellworld,login

urlpatterns = [
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout', views.logout_view),
    url(r'^demand', views.get_demand,name='demand'),
    url(r'^superdemand',views.super_demand),
    url(r'^checkdemand',views.show_demand),
    url(r'^selectdemand',views.selectdemand,name='selectdemand'),
    url(r'^hello', views.getHellworld),
    url(r'^register$', views.register_view, name='register'),
    # url(r'^login',login),
    # url(r'^index',getform),
    # url(r'^hello',getHellworld),
    url(r'^admin/', admin.site.urls),
    # url(r'^form/$',getform,name='go_form')
]
