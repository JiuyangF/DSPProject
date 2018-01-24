# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib import auth
from controller.core.public import *
import json

# Create your views here.


@login_required
def index(request):
    # 首页
    nowuser = auth.get_user(request)
    return render_to_response('index.html', locals())


def page_not_found(request):
    return render_to_response("404.html")


def permission_denied(request):
    return render_to_response("403.html")


@login_required
def get_username(request):
    # 获取当前登陆的用户名
    nowuser = auth.get_user(request)
    username = nowuser.get_username()
    response = HttpResponse()
    response.write(json.dumps(username))
    return response


@login_required
def check_permission(request):
    # 检测用户权限
    # print(request,'check_permission 少时诵诗书所所所所所所所所所所所所所所所所所所所所所所所所所所所所')
    nowuser = auth.get_user(request)
    cur = Currency(request)
    permission = cur.rq_post('permission')
    status = 0 if nowuser.has_perm(permission) else 1
    response = HttpResponse()
    response.write(json.dumps({'status': status}))
    return response