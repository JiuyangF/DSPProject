# -*- coding: UTF-8 -*-
from django.conf.urls import url
# import sheduled_tasks.views
# from scheduled_tasks import views

from message import views

urlpatterns = [
    # url(r'^demand/$', views.get_demand, name='demand'),
    url(r'^submit_demand/$', views.submit_demand, name='submit_demand'), #外部用户提交信息页面
    url(r'^add_demand_data/$',views.add_demand_data),  #外部用户添加新需求数据入库url
    url(r'^show_demand/$', views.show_demands, name='show_demand'), #外部用户查看已提交需求页面
    url(r'^out_demand_show/$', views.out_demand_show, name='out_demand_show'), #外部用户查看已提交需求的方法
    url(r'^upload_ajax/$', views.upload_ajax, name='upload_ajax'),  # 需求文档上传方法
    url(r'^update_demand/(?P<id>\d+)$', views.update_demand, name='update_demand'),  # 需求文档上传方法
    url(r'^update_demand_data/$', views.update_demand_data, name='update_demand_data'),
    # url(r'^checkdemand/$', views.show_demand),
    # url(r'^selectdemand/$', views.selectdemand, name='selectdemand'),


    url(r'^need_approval/$', views.need_approval, name='need_approval'),  #管理员查看待审核需求页面
    url(r'^approved/$', views.approved, name='approved'), #管理员查看已审核需求页面
    url(r'^demand_get_data/$', views.demand_get_data, name='demand_get_data'), #获取管理员可查看的需求的方法
    url(r'^mod_approved/(?P<id>\d+)/$', views.mod_approved),  # 修改查看已审核需求数据
    url(r'^get_demand_byid/$', views.get_demand_byid),  # 根据id返回需求信息

]