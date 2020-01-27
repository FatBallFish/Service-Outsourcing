from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.faces.models import FaceData
from apps.realauth.models import RealAuth
from django.utils.html import format_html
from Hotel import settings


class BaseModel(models.Model):
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)
    update_time = models.DateTimeField(verbose_name="更新时间", default=datetime.now)

    class Meta:
        abstract = True  # 设置为静态表，不会被生成


# Create your models here.

class Users(AbstractUser):
    nickname = models.CharField(verbose_name="昵称", max_length=20, blank=True, null=True)
    phone = models.CharField(verbose_name="手机号", max_length=11, unique=True)
    image = models.ImageField(verbose_name="用户头像", upload_to='users', default="users/default.jpg")
    real_auth = models.ForeignKey(verbose_name="实名认证", to=RealAuth, on_delete=models.SET_NULL, blank=True, null=True)
    face = models.ForeignKey(verbose_name="人脸数据", to=FaceData, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username + "({})".format(self.nickname)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        db_table = "users"

    info_html = "<div>{}</div>"

    def auth_type(self):
        id_type = {"sfz": "身份证", "other": "其他"}
        return format_html(self.info_html, id_type[self.real_auth.id_type])

    auth_type.short_description = "证件类型"

    def auth_ID(self):
        return format_html(self.info_html, self.real_auth.ID)

    auth_ID.short_description = "证件号"

    def auth_name(self):
        return format_html(self.info_html, self.real_auth.name)

    auth_name.short_description = "姓名"

    def auth_gender(self):
        return format_html(self.info_html, self.real_auth.gender)

    auth_gender.short_description = "性别"

    def auth_nation(self):
        return format_html(self.info_html, self.real_auth.nation)

    auth_nation.short_description = "民族"

    def auth_age(self):
        today = datetime.now().date()
        differ = ((today - self.real_auth.birthday) // 365).days
        return format_html(self.info_html, differ)

    auth_age.short_description = "年龄"

    def auth_birthday(self):
        return format_html(self.info_html, self.real_auth.birthday)

    auth_birthday.short_description = "出生年月"

    def auth_address(self):
        return format_html(self.info_html, self.real_auth.address)

    auth_address.short_description = "住址"

    def auth_organization(self):
        return format_html(self.info_html, self.real_auth.organization)

    auth_organization.short_description = "签发机关"

    def auth_date(self):
        date_str = "{} - {}".format(self.real_auth.date_start, self.real_auth.date_end)
        return format_html(self.info_html, date_str)

    auth_date.short_description = "有效期"

    def face_name(self):
        return format_html(self.info_html, self.face.name)

    face_name.short_description = "真实姓名"

    def face_gender(self):
        if self.face.gender == 'male':
            gender = "先生"
        else:
            gender = "女士"
        return format_html(self.info_html, gender)

    face_gender.short_description = "性别"

    def face_content(self):
        return format_html(self.info_html, self.face.content)

    face_content.short_description = "备注"

    def face_sign(self):
        return format_html(self.info_html, self.face.sign)

    face_sign.short_description = "特征值"

    def face_pic(self):
        if self.face.if_local is True:
            return format_html('<img src="/media/{}" style="width:100px;height:auto">', self.face.pic)
        else:
            return format_html('<img src="{}" style="width:100px;height:auto">', self.face.cos_pic)

    face_pic.short_description = "注册图片"  # 显示在列表表头的描述

    def group_id(self):
        return format_html(self.info_html, self.face.faces_group.id)

    group_id.short_description = "人员库id"

    def group_name(self):
        return format_html(self.info_html, self.face.faces_group.name)

    group_name.short_description = "人员库名称"

    def group_content(self):
        return format_html(self.info_html, self.face.faces_group.content)

    group_content.short_description = "人员库描述"
