# Generated by Django 2.0.1 on 2018-03-07 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataBaseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='名称')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('host', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='主机')),
                ('user', models.CharField(blank=True, max_length=255, null=True, verbose_name='用户')),
                ('passwd', models.CharField(blank=True, max_length=255, null=True, verbose_name='密码')),
                ('db', models.CharField(blank=True, max_length=255, null=True, verbose_name='数据库实例')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='数据库类型')),
            ],
            options={
                'db_table': 'databaseinfo',
            },
        ),
        migrations.CreateModel(
            name='ScheduledTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('viewTask', '查看定时任务'), ('editTask', '修改定时任务')),
                'db_table': 'scheduledTask',
            },
        ),
    ]
