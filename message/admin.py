from django.contrib import admin
#添加数据库表到admin实现后台管理
from message.models import SpiderDemandInfo,DemandColumnInfo,UserInfo
admin.site.register(SpiderDemandInfo)
admin.site.register(DemandColumnInfo)
# admin.site.register(UserInfo)
# Register your models here.
