# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class UserInfo(models.Model):
    user_name = models.CharField(max_length=30)
    user_pass = models.CharField(max_length=40)

class DemandColumnInfo(models.Model):
    dc_id = models.AutoField(db_column='DC_id', primary_key=True)  # Field name made lowercase.
    d = models.ForeignKey('SpiderDemandInfo', models.DO_NOTHING, db_column='D_id')  # Field name made lowercase.
    column_name_cn = models.CharField(max_length=30)
    column_name_en = models.CharField(max_length=30, blank=True, null=True)
    extraction_rule = models.CharField(max_length=100, blank=True, null=True)
    extraction_type = models.CharField(max_length=20, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'demand_column_info'

class SpiderDemandInfo(models.Model):
    d_id = models.AutoField(db_column='D_id', primary_key=True)  # Field name made lowercase.
    d_code = models.CharField(db_column='D_code', max_length=32)  # Field name made lowercase.
    demand_name = models.CharField(max_length=30)
    demand_department = models.CharField(max_length=20)
    priority_level = models.CharField(max_length=10, blank=True, null=True)
    channel_name = models.CharField(max_length=30)
    data_type = models.CharField(max_length=20)
    proposer = models.CharField(max_length=20, blank=True, null=True)
    is_app = models.IntegerField()
    start_url = models.CharField(max_length=300, blank=True, null=True)
    spider_rate = models.CharField(max_length=10, blank=True, null=True)
    upload_doc = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    examine_status = models.IntegerField()
    task_executor = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'spider_demand_info'
