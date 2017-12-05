from django.db import models
from django.db import connection


# Create your models here.

class AdminUser(models.Model):
    # def get_user_info(self):
    #     pass
    def __init__(self):
        self.cur = connection.cursor()

    def get_name(self):
        select_sql = ""
        self.cur(select_sql)
    # name=models.CharField(max_length=20)