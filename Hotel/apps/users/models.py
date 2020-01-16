from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from Hotel import settings


class BaseModel(models.Model):
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)
    update_time = models.DateTimeField(verbose_name="更新时间", default=datetime.now)

    class Meta:
        abstract = True  # 设置为静态表，不会被生成


# Create your models here.

class Users(AbstractUser):
    nickname = models.CharField(verbose_name="昵称", max_length=20, null=True)
    phone = models.CharField(verbose_name="手机号", max_length=11, unique=True)
    gender = models.CharField(verbose_name="性别", choices=(("male", "先生"), ("female", "女士")), max_length=6, null=True)
    image = models.ImageField(verbose_name="用户头像", upload_to='users', default="users/default.jpg")

    def __str__(self):
        return self.username + "({})".format(self.last_name + self.first_name)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        db_table = "users"
