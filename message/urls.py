# -*- coding: UTF-8 -*-
from django.conf.urls import url
# import sheduled_tasks.views
# from scheduled_tasks import views
from message import views

urlpatterns = [
    url(r'^demand/$', views.get_demand, name='demand'),
    url(r'^submit_demand/$', views.submit_demand, name='submit_demand'),
    url(r'^show_demand/$', views.show_demands, name='show_demand'),
    url(r'^out_demand_show/$', views.out_demand_show, name='out_demand_show'),
    url(r'^checkdemand/$', views.show_demand),
    url(r'^selectdemand/$', views.selectdemand, name='selectdemand'),
    url(r'^need_approval/$', views.need_approval, name='need_approval'),
    url(r'^approved/$', views.approved, name='approved'),
    url(r'^demand_get_data/$', views.demand_get_data, name='demand_get_data'),
    url(r'^mod_demand_data/(?P<id>\d+)/$', views.mod_demand_data),  # 修改周期任务 页面

]