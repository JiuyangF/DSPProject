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
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
# from django.contrib.auth.views import logout
from django.contrib.auth.views import login
from message import views
admin.autodiscover()
from DSPProject.views import *

# from message.views import getform,getHellworld,login

urlpatterns = [
    # url(r'^login', views.login_view, name='login'),
    # url(r'^logout', views.logout),
    url(r'login',login, {'template_name': 'login.htm'},name='login'),
    url(r'^index/$', index),  # 首页
    url(r'^$', index, name='index'),
    url(r'^accounts/login/$', login, {'template_name': 'login.htm'},name='login'),
    url(r'^register$', views.register_view, name='register'),
    url(r'^accounts/logout/$', views.logout,name='logout'),



    url(r'^get_username/$', get_username),  # 获取当前登陆用户名
    url(r'^check_permission/$', check_permission),  # 检测用户权限


    url(r'^scheduled_tasks/', include('sheduled_tasks.urls')),
    url(r'^spiders_scheduled/', include('spiders_scheduled.urls')),
    url(r'^message/', include('message.urls')),
    url(r'^admin/', admin.site.urls)
    # url(r'^form/$',getform,name='go_form')
]