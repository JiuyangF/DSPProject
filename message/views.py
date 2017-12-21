from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from message.models import DemandColumnInfo,SpiderDemandInfo
from DSPProject import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# 第四个是 auth中用户权限有关的类。auth可以设置每个用户的权限。
import os
from .form import UserForm,DemandForm

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


def get_demand(req):
    context = {}
    if req.method == 'POST':
        form = DemandForm(req.POST)
        print(form.is_valid())
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
            try:
                demands = SpiderDemandInfo.objects.get(start_url=start_urls)
            except:
                demands = False
            if demands:
                return HttpResponse("已提交，请勿重复提交")
            else:
                demands_save = SpiderDemandInfo(demand_department=department,priority_level=priority,
                                                channel_name = channel_name,data_type=data_type,
                                                spider_rate=rate,upload_doc=fname,comment=dem_com,
                                                is_app=is_app,start_url=start_urls,status=1,examine_status=0)
                demands_save.save()
                print("okokokokokokokokokokokokokokokokok")
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
            context = {'isLogin': False,'pawd':False}
            return render(req, 'demand.html', context)
    else:
        context = {'isLogin': False,'pswd':True}
    return render(req, 'demand.html', context)



#登出
def logout_view(req):
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
     info = models.UserInfo.objects.all()[:10]
     print(info)
     print('llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll')
     context = {"dd":"ds",'info':info}
     return HttpResponse(tem.render(context))

