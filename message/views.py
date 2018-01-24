import uuid

import time
from django.shortcuts import render, redirect, render_to_response
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from message.models import DemandColumnInfo, SpiderDemandInfo, UserInfo
from DSPProject import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# 第四个是 auth中用户权限有关的类。auth可以设置每个用户的权限。
import os
from .form import UserForm,DemandForm,SuperDemand,DemandSelect

#注册
@csrf_exempt
def register_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 判断用户是否存在
            user = auth.authenticate(username = username,password = password)
            if user:
                context['userExit']=True
                return render(req, 'register.html', context)


            #添加到数据库（还可以加一些字段的处理）
            user = User.objects.create_user(username=username, password=password)
            user.save()

            #添加到session
            req.session['username'] = username
            #调用auth登录
            auth.login(req, user)
            #重定向到首页
            return redirect('/hello')
    else:
        context = {'isLogin':False}
    #将req 、页面 、以及context{}（要传入html文件中的内容包含在字典里）返回
    return  render(req,'register.html',context)

#登陆
@csrf_exempt
def login_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获取表单用户密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #获取的表单数据与数据库进行比较
            user = authenticate(username = username,password = password)
            if user:
                #比较成功，跳转index
                auth.login(req,user)
                req.session['username'] = username
                return redirect('/hello')
            else:
                #比较失败，还在login
                context = {'isLogin': False,'pawd':False}
                return render(req, 'login.html', context)
    else:
        context = {'isLogin': False,'pswd':True}
    return render(req, 'login.html', context)


def handle_uploaded_file(f):
    """
    需求文档上传功能
    :param f:
    :return:
    """
    print(f.name,f.chunks(),"writesssssssssssssssssssssssssssssssssss")
    # with open(f.chunks(),'r') as des:
    #     print(des)
    filename = f.name
    path = settings.FILE_STORE
    # path='D:/work/'     #上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+filename,'wb+')as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def get_demand(req):
    """
    需求上传方法，实现需求入库功能
    :param req:
    :return:
    """
    context = {}
    if req.method == 'POST':
        form = DemandForm(req.POST)
        # print(form.is_valid())
        if form.is_valid():
        #获取需求信息表单
            department = form.cleaned_data['department']
            priority = form.cleaned_data['priority']
            channel_name = form.cleaned_data['channel_name']
            data_type = form.cleaned_data['data_type']
            is_app = form.cleaned_data['is_app']
            start_urls = form.cleaned_data['start_url']
            rate = form.cleaned_data['rate']
            dem_com = form.cleaned_data['dem_com']
            de_data = form.cleaned_data['de_data']
            print(de_data,department,data_type,is_app,type(is_app))
            handle_uploaded_file(req.FILES['file'])
            fname = req.FILES['file'].name
            d_code = str(uuid.uuid1()).replace('-', '')
            de_name = channel_name+"_"+data_type
            proposer = form.cleaned_data['proposer']
            try:
                demands = SpiderDemandInfo.objects.get(start_url=start_urls,demand_name =de_name,proposer=proposer)
            except:
                demands = False
            if demands:
                return render(req, 'demand.html', context={'isComplete': True})
            else:
                a = SpiderDemandInfo.objects.latest('d_id')
                max_id = a.d_id + 1
                demands_save = SpiderDemandInfo(d_code=d_code,demand_name = de_name,demand_department=department,priority_level=priority,
                                                channel_name = channel_name,proposer=proposer,data_type=data_type,
                                                spider_rate=rate,upload_doc=fname,comment=dem_com,
                                                is_app=is_app,start_url=start_urls,status=1,examine_status=0)

                list_de_data = str(de_data).replace("；",';').strip(';').split(';')
                # d = SpiderDemandInfo.objects.get(d_code=d_code).d_id
                for demand_data in list_de_data:
                    # 返回对象 = 子表(子表外键=母表.objects.get(母表字段=数据), 子表字段=要添加的数据)
                    # 返回对象.save()
                    # DemandColumnInfo.objects.create(,column_name_cn=demand_data)
                    demand_column = DemandColumnInfo(d_id=max_id,column_name_cn=demand_data)
                    demand_column.save()
                demands_save.save()
                de_time = time.strftime("%Y-%m-%d")
                post_list = [{"channel_name":channel_name,"department":department,"data_type":data_type,"de_time":de_time,"status":"待审核"}]
                # print(max_id,"max id")
                # print("okokokokokokokokokokokokokokokokok")
            # return HttpResponse("提交成功")
            return render(req, 'checkdemand.html', context={'isComplete': False,'post_list':post_list})
            # #获取的表单数据与数据库进行比较
            # user = authenticate(username = username,password = password)
            # if user:
            #     #比较成功，跳转index
            #     auth.login(req,user)
            #     req.session['username'] = username
            #     return redirect('/hello')
        else:
            #提交失败，还在demand
            # context = {'isLogin': False,'pawd':False}
            return render(req, 'demand.html', context={'isComplete': True})
    else:
        # context = {'isLogin': False,'pswd':True}
        return render(req, 'demand.html', context={'isComplete': False})

@login_required
def show_demand(req):
    """
    显示所有需求
    :param req:
    :return:
    """
    post_list = []
    status_dict = {1:'待审批',0:'未通过',2:"已通过"}
    a_list = SpiderDemandInfo.objects.all()
    for a in a_list:
        channel_name = a.channel_name
        department = a.demand_department
        data_type = a.data_type
        de_time = a.create_time.strftime("%Y-%m-%d")
        status = status_dict[a.status]
        dict_demand = {"channel_name": channel_name, "department": department, "data_type": data_type, "de_time": de_time,
         "status": status}
        # print(dict_demand)
        post_list.append(dict_demand)
    # post_list = [{"channel_name": channel_name, "department": department, "data_type": data_type, "de_time": de_time,
    #               "status": "待审核"}]

    return render(req, 'checkdemand.html', context={'post_list': post_list})
    # pass

@login_required
def selectdemand(req):
    """
    显示筛选后的需求信息

    :param req:
    :return:
    """
    post_list = []
    status_dict = {1: '待审批', 0: '未通过', 2: "已通过"}
    if req.POST:
        form = DemandSelect(req.POST)
        if form.is_valid():
            # 获取表单用户密码
            createtime = form.cleaned_data['create_time']
            channel_name = form.cleaned_data['channel_name']
        # createtime = req.POST['create_time']
            print(createtime)
        # channel_name = req.POST['channel_name']

            a_list = SpiderDemandInfo.objects.filter(create_time__startswith=createtime,channel_name=channel_name)
            for a in a_list:
                channel_name = a.channel_name
                department = a.demand_department
                data_type =  a.data_type
                de_time = a.create_time.strftime("%Y-%m-%d")
                status = status_dict[a.status]
                dict_demand = {"channel_name": channel_name, "department": department, "data_type": data_type, "de_time": de_time,
                 "status": status}
                # print(dict_demand)
                post_list.append(dict_demand)
            # post_list = [{"channel_name": channel_name, "department": department, "data_type": data_type, "de_time": de_time,
            #               "status": "待审核"}]

        return render(req, 'checkdemand.html', context={'post_list': post_list})
    else:
        a_list = SpiderDemandInfo.objects.all()
        for a in a_list:
            channel_name = a.channel_name
            department = a.demand_department
            data_type = a.data_type
            de_time = a.create_time.strftime("%Y-%m-%d")
            status = status_dict[a.status]
            dict_demand = {"channel_name": channel_name, "department": department, "data_type": data_type,
                           "de_time": de_time,
                           "status": status}
            # print(dict_demand)
            post_list.append(dict_demand)
        # post_list = [{"channel_name": channel_name, "department": department, "data_type": data_type, "de_time": de_time,
        #               "status": "待审核"}]

        return render(req, 'checkdemand.html', context={'post_list': post_list})
    #
    #     return render(req, 'checkdemand.html', context={'post_list': post_list})

def super_demand(req):
    if req.method == 'POST':
        form = SuperDemand(req.POST)
        print(form.is_valid())
        if form.is_valid():
        #获取需求信息表单
            department = form.cleaned_data['department']
            priority = form.cleaned_data['priority']
            channel_name = form.cleaned_data['channel_name']
            data_type = form.cleaned_data['data_type']
            # is_app = form.cleaned_data['is_app']
            # start_urls = form.cleaned_data['start_url']
            # rate = form.cleaned_data['rate']
            # dem_com = form.cleaned_data['dem_com']
            # de_data = form.cleaned_data['de_data']
            # print(de_data,department,data_type,is_app,type(is_app))
            # handle_uploaded_file(req.FILES['file'])
            # fname = req.FILES['file'].name
            # d_code = str(uuid.uuid1()).replace('-', '')
            # de_name = channel_name+"_"+data_type
            # proposer = form.cleaned_data['proposer']
            # try:
            #     demands = SpiderDemandInfo.objects.get(start_url=start_urls)
            # except:
            #     demands = False
            # if demands:
            #     return HttpResponse("已提交，请勿重复提交")
            # else:
            #     a = SpiderDemandInfo.objects.latest('d_id')
            #     max_id = a.d_id + 1
            #     demands_save = SpiderDemandInfo(d_code=d_code,demand_name = de_name,demand_department=department,priority_level=priority,
            #                                     channel_name = channel_name,proposer=proposer,data_type=data_type,
            #                                     spider_rate=rate,upload_doc=fname,comment=dem_com,
            #                                     is_app=is_app,start_url=start_urls,status=1,examine_status=0)
            #     demands_save.save()
            #     print(max_id,"max id")
                # print("okokokokokokokokokokokokokokokokok")
            return HttpResponse("提交成功")

            # #获取的表单数据与数据库进行比较
            # user = authenticate(username = username,password = password)
            # if user:
            #     #比较成功，跳转index
            #     auth.login(req,user)
            #     req.session['username'] = username
            #     return redirect('/hello')
        else:
            #提交失败，还在demand

            return HttpResponse("提交失败")
    else:
        form = SuperDemand()
    return render(req,'superdemand.html', {'form': form})

#登出
@csrf_exempt
def logout(req):
    #清理cookie里保存username
    auth.logout(req)
    return redirect('/login')

# Create your views here.

def getform(request):
     context = {}
     context['hello'] = 'Hello World!'
     return render(request, 'temp.html', context)

def getHellworld(request):
     return HttpResponse('hello world')

def login(request):
     tem = loader.get_template('temp.html')
     info = UserInfo.objects.all()[:10]
     print(info)
     print('llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll')
     context = {"dd":"ds",'info':info}
     return HttpResponse(tem.render(context))

