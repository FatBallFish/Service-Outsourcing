from django.db import models
from django.utils.html import format_html

from datetime import datetime


# Create your models here.
class RealAuth(models.Model):
    id_type = models.CharField(verbose_name="证件类型", choices=(("sfz", "中国大陆身份证"), ("other", "其他")), max_length=10,
                               default="sfz")
    ID = models.CharField(verbose_name="证件号", max_length=18, primary_key=True)
    name = models.CharField(verbose_name="姓名", max_length=30)
    gender = models.CharField(verbose_name="性别", choices=(('male', "先生"), ('female', "女士")), max_length=6)
    nation = models.CharField(verbose_name="民族", max_length=10, blank=True, null=True)
    birthday = models.DateField(verbose_name="出生年月")
    address = models.TextField(verbose_name="住址", max_length=100, blank=True, null=True)
    organization = models.CharField(verbose_name="签发机关", max_length=30, blank=True, null=True)
    date_start = models.DateField(verbose_name="有效期_始", blank=True, null=True)
    date_end = models.DateField(verbose_name="有效期_末", blank=True, null=True)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)
    update_time = models.DateTimeField(verbose_name="更新时间", default=datetime.now)

    class Meta:
        verbose_name = "实名认证库"
        verbose_name_plural = verbose_name
        db_table = "realauth"

    def __str__(self):
        return "{}({})".format(self.name, self.gender)

    info_html = "<div>{}</div>"
