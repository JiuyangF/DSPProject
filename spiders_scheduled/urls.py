# -*- coding: UTF-8 -*-
from django.conf.urls import url
# import sheduled_tasks.views
# from scheduled_tasks import views
from spiders_scheduled import views

urlpatterns = [

    url(r'^spiders_task/$', views.spiders_task),  # 周期任务
    url(r'^add_spiders_task/$', views.add_spiders_task),  # 新增 脚本周期任务
    url(r'^get_task_spiders/$', views.get_task_spiders),  # 获取任务脚本列表 get scripts tasks list
    url(r'^get_task_template/$', views.get_task_template),  # 获取任务模板列表 get tasks list

    url(r'^add_periodic_task_spiders/$', views.add_periodic_task_spiders),  # 提交  新增脚本周期任务 数据

]