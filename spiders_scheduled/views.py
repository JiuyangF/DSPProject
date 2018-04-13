
# Create your views here.
import json

from celery import registry
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render_to_response,render
from djcelery import loaders
from djcelery.models import CrontabSchedule
from djcelery.schedulers import DatabaseScheduler

from controller.core.public import Currency
from message.models import SpiderDemandInfo


@login_required
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
def spiders_task(request):
    #查询脚本周期任务数据
    return render(request, 'spiders_scheduled/spiders_task.html', locals())

@login_required
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
@permission_required('sheduled_tasks.editTask', raise_exception=PermissionDenied)
def add_spiders_task(request):
    # 新增 脚本周期任务
    return render_to_response('spiders_scheduled/add_spiders_task.html', locals())


@login_required
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
def get_task_spiders(request):
    #获取脚本列表
    tasks_list = []
    loaders.autodiscover()
    response = HttpResponse()
    tasks = SpiderDemandInfo.objects.all().values_list('demand_name','spiders_file')
    # tasks = list(sorted(registry.tasks.regular().keys()))
    for line in tasks:
        if line[1] != None:
            tasks_list.append(line[0]+'.'+line[1])
    # print(tasks, '***---tasks---***')
    # print(tasks_list, '***---tasks---***')
    response.write(json.dumps(tasks_list))
    return response


@login_required
@permission_required('sheduled_tasks.editTask', raise_exception=PermissionDenied)
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
def add_periodic_task_spiders(request):
    # 提交新增周期任务数据
    response = HttpResponse()
    cur = Currency(request)
    rq_post = getattr(cur, 'rq_post')
    jdata = rq_post('data')
    data = json.loads(jdata)
    task_spiders = data['task_spiders']
    crontab = data['crontab']
    is_enable = data['is_enable']
    is_encrypt = data['is_encrypt']
    # is_sensitive = data['is_sensitive']
    task_name = data['task_name']
    task_template = data['task_template']

    #将数据信息导入到celery的执行对列中
    schedule = CrontabSchedule.objects.get(pk=crontab).schedule
    create_or_update_task = DatabaseScheduler.create_or_update_task
    schedule_dict = {
        'schedule': schedule,
        'task': task_template,
        'args': [task_spiders],
        'enabled': is_enable
    }
    create_or_update_task(task_name, **schedule_dict)
    # mail_excel(mail_header, task_name, sql_list, **mailpara)
    response.write(json.dumps({'status': 0, 'msg': ['操作成功']}))
    return response


@login_required
@permission_required('sheduled_tasks.viewTask', raise_exception=PermissionDenied)
def get_task_template(request):
    irrelevant_tasks = ['YinguOnline.celery.debug_task',
                        'backup_ygolp',
                        'celery.backend_cleanup',
                        'celery.chain',
                        'celery.chord',
                        'celery.chord_unlock',
                        'celery.chunks',
                        'celery.group',
                        'celery.map',
                        'celery.starmap',
                        'runing_invest_script',
                        'DSPProject.celery.debug_task']

    loaders.autodiscover()
    response = HttpResponse()
    tasks = list(sorted(registry.tasks.regular().keys()))
    for t in irrelevant_tasks:
        try:
            tasks.remove(t)
        except:
            continue
    # print(tasks)
    response.write(json.dumps(tasks))
    return response