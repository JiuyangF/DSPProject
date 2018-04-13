import json
import uuid

import time

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, render_to_response
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from controller.core.public import Currency
from message.models import DemandColumnInfo, SpiderDemandInfo, UserInfo
from DSPProject import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
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
            return redirect('out_page/checkdemand.html')
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

#登出
@csrf_exempt
def logout(req):
    #清理cookie里保存username
    auth.logout(req)
    return redirect('/login')

@login_required
#外部需求方接口及方法
def submit_demand(req):
    """
    跳转到用户提交新需求的页面
    :param req:
    :return:
    """
    return render_to_response('out_page/submit_demand.html', locals())

@login_required
def update_demand(req,id):
    return render_to_response('out_page/update_demand.html', locals())

@login_required
def update_demand_data(req):
    """
        实现需求更新功能
        :param req:
        :return:
        """
    response = HttpResponse()
    cur = Currency(req)
    rq_post = getattr(cur, 'rq_post')
    data = json.loads(rq_post('data'))
    _id = data['_id']
    # username = data['username']
    # department = data['department']
    # channel_name = data['channel_name']
    # data_type = data['data_type']
    is_app = data['is_app']
    start_url = data['start_url']
    rate = data['rate']
    priority = data['priority']
    column = data['column']
    comment = data['comment']
    file_name = data['file_name']
    d_code = str(uuid.uuid1()).replace('-', '')
    # de_name = channel_name + "_" + data_type
    try:
        status = 0
        SpiderDemandInfo.objects.filter(d_id=_id).update(priority_level=priority,
                                        spider_rate=rate, upload_doc=file_name, comment=comment,
                                        is_app=is_app, start_url=start_url, status=1, examine_status=0)
        DemandColumnInfo.objects.filter(d_id=_id).delete()
        list_de_data = str(column).replace("；", ';').strip(';').split('\n')
        # d = SpiderDemandInfo.objects.get(d_code=d_code).d_id
        for demand_data in list_de_data:
            # 返回对象 = 子表(子表外键=母表.objects.get(母表字段=数据), 子表字段=要添加的数据)
            # 返回对象.save()
            # DemandColumnInfo.objects.create(,column_name_cn=demand_data)
            demand_column = DemandColumnInfo(d_id=_id, column_name_cn=demand_data)
            demand_column.save()
        msg = ['已完成更新']
    except:
        status = 1
        msg = ['更新失败']
    response.write(json.dumps({"status": status, 'msg': msg}))
    return response

@login_required
def add_demand_data(req):
    """
    实现新需求提交功能
    :param req:
    :return:
    """
    response = HttpResponse()
    cur = Currency(req)
    rq_post = getattr(cur,'rq_post')
    data = json.loads(rq_post('data'))
    username = data['username']
    department = data['department']
    channel_name = data['channel_name']
    data_type = data['data_type']
    is_app = data['is_app']
    start_url = data['start_url']
    rate = data['rate']
    priority = data['priority']
    de_field = data['de_field']
    comment = data['comment']
    file_name = data['file_name']
    d_code = str(uuid.uuid1()).replace('-', '')
    de_name = channel_name + "_" + data_type
    try:
        demands = SpiderDemandInfo.objects.get(start_url=start_url, demand_name=de_name, proposer=username)
    except:
        demands = False
    if demands:
        status = 1
        msg = ['需求信息已存在']
    else:
        #填入插入的语句
        a = SpiderDemandInfo.objects.latest('d_id')
        max_id = a.d_id + 1
        demands_save = SpiderDemandInfo(d_code=d_code, demand_name=de_name, demand_department=department,
                                        priority_level=priority,
                                        channel_name=channel_name, proposer=username, data_type=data_type,
                                        spider_rate=rate, upload_doc=file_name, comment=comment,
                                        is_app=is_app, start_url=start_url, status=1, examine_status=0)

        list_de_data = str(de_field).replace("；", ';').strip(';').split('\n')
        # d = SpiderDemandInfo.objects.get(d_code=d_code).d_id
        for demand_data in list_de_data:
            # 返回对象 = 子表(子表外键=母表.objects.get(母表字段=数据), 子表字段=要添加的数据)
            # 返回对象.save()
            # DemandColumnInfo.objects.create(,column_name_cn=demand_data)
            demand_column = DemandColumnInfo(d_id=max_id, column_name_cn=demand_data)
            demand_column.save()
        demands_save.save()
        status = 0
        msg = ['操作成功']
    response.write(json.dumps({"status": status,'msg': msg}))
    return response

@login_required
def upload_ajax(request):
    """
    实现需求文档上传功能
    :param request:
    :return:
    """
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        handle_uploaded_file(file_obj)
        return HttpResponse('OK')

@login_required
def show_demands(req):
    """
    实现用户需求信息展示页面
    :param req:
    :return:
    """
    return render_to_response('out_page/show_demand.html',locals())

@login_required
def out_demand_show(req):
    """
    外部用户需求信息展示页面
    :param req:
    :return:
    """
    nowuser = auth.get_user(req)
    username = nowuser.get_username()
    response = HttpResponse()
    num_dict = {1:'是',0:'否'}
    status_dict = {1: '待审批', 0: '未通过', 2: "已通过"}
    spider_demand_obj = SpiderDemandInfo.objects.filter(proposer=username)
    crontabs_stf = [{'id': c.d_id, 'channel_name': c.channel_name,'demand_department': c.demand_department,
                     'data_type': c.data_type,'demand_name': c.demand_name,'priority_level': c.priority_level,
                     'create_time': c.create_time.strftime("%Y-%m-%d"),'is_app':num_dict[c.is_app],
                     'start_url': c.start_url,'update_time': c.update_time.strftime("%Y-%m-%d"),'status': status_dict[c.status]} for c in spider_demand_obj]
    response.write(json.dumps(crontabs_stf))
    return response

"""

上方为面向外部用户的接口及方法

"""

#demand相关方法 新增需求的方法
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
                return render(req, 'out_page/demand.html', context={'isComplete': True})
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
            return render(req, 'out_page/checkdemand.html', context={'isComplete': False,'post_list':post_list})
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
            return render(req, 'out_page/demand.html', context={'isComplete': True})
    else:
        # context = {'isLogin': False,'pswd':True}
        return render(req, 'out_page/demand.html', context={'isComplete': False})

#面向用户的信息查询页面
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

    return render(req, 'out_page/checkdemand.html', context={'post_list': post_list})
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

        return render(req, 'out_page/checkdemand.html', context={'post_list': post_list})
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

        return render(req, 'out_page/checkdemand.html', context={'post_list': post_list})
    #
    #     return render(req, 'checkdemand.html', context={'post_list': post_list})

@login_required
@permission_required('sheduled_tasks.editTask', raise_exception=PermissionDenied)
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
def need_approval(req):
    """
    待审核需求数据
    :param req:
    :return:
    """
    return render_to_response('message/approval_demand.html', locals())

@login_required
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
def approved(req):
    """
    已审核需求数据
    :param req:
    :return:
    """
    return render_to_response('message/approved.html', locals())


@login_required
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
def demand_get_data(req):
    response = HttpResponse()
    status = req.GET.get('status')
    if status == '1':
        list_status = [1]
    else:
        list_status = [0,2]
    num_dict = {1:'是',0:'否'}
    status_dict = {1: '待审批', 0: '未通过', 2: "已通过"}
    spider_demand_obj = SpiderDemandInfo.objects.filter(status__in=list_status)
    crontabs_stf = [{'id': c.d_id, 'channel_name': c.channel_name,'demand_department': c.demand_department,
                     'data_type': c.data_type,'demand_name': c.demand_name,'priority_level': c.priority_level,
                     'create_time': c.create_time.strftime("%Y-%m-%d"),'is_app':num_dict[c.is_app],
                     'start_url': c.start_url,'proposer': c.proposer,'status': status_dict[c.status]} for c in spider_demand_obj]
    response.write(json.dumps(crontabs_stf))
    return response

#实现需求信息展示及操作功能
@login_required
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
@permission_required('sheduled_tasks.editTask', raise_exception=PermissionDenied)
def mod_approved(req,id):
    return render_to_response('message/mod_approved.html', locals())


@login_required
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
@permission_required('sheduled_tasks.editTask', raise_exception=PermissionDenied)
def get_demand_byid(req):
    """
    根据id返回需求信息
    :param req:
    :return:
    """
    response = HttpResponse()
    _id = req.POST.get('_id')
    num_dict = {1:'是',0:'否'}
    status_dict = {1: '待审批', 0: '未通过', 2: "已通过"}
    spider_demand_obj = SpiderDemandInfo.objects.filter(d_id=_id)
    demand_column_obj = DemandColumnInfo.objects.filter(d_id=_id)
    column_list = [col.column_name_cn for col in demand_column_obj]
    column = '\n'.join(column_list)
    demand_stf = {}
    for c in spider_demand_obj:
        demand_stf = {'id': c.d_id, 'channel_name': c.channel_name,'demand_department': c.demand_department,
                     'data_type': c.data_type,'demand_name': c.demand_name,'priority_level': c.priority_level,
                     'create_time': c.create_time.strftime("%Y-%m-%d"),'is_app':num_dict[c.is_app],'spider_rate':c.spider_rate,
                     'start_url': c.start_url,'proposer': c.proposer,'status': status_dict[c.status],'comment':c.comment,'column':column}
    response.write(json.dumps(demand_stf))
    return response




def mod_demand_data_show(req):


    pass



#通用方法
def handle_uploaded_file(f):
    """
    需求文档上传功能
    :param f:
    :return:
    """
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
    f.close()

# Create your views here.


