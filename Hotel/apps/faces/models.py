from datetime import datetime
from django.db import models
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.html import format_html

from extral_apps import MD5
from extral_apps.m_cos import py_cos_main as COS
from Hotel import settings

from apps.users.models import BaseModel, Users


@deconstructible
class CosStorage(Storage):
    path = ""

    def __init__(self, path):
        self.path = path + "/"

    def save(self, name, content, max_length=None):
        suffix = name.split('.')[-1]
        img_data = content.read()
        # print(img_data)
        key = self.path + MD5.md5_bytes(content.read()) + "." + suffix
        # print(os.path.join(settings.BASE_DIR,"Program","NIAECv2",settings.MEDIA_URL,key))
        # with open(os.path.join(settings.BASE_DIR,"Program","NIAECv2",settings.MEDIA_URL,key),"wb") as f:
        #     f.write(img_data)
        try:
            COS.bytes_upload(body=img_data, key=key)
        except Exception as e:
            raise
        return settings.COS_ROOTURL + key

    def url(self, name):
        return name


# Create your models here.
class FaceGroup(BaseModel):
    group_id = models.IntegerField(verbose_name="人员库ID", primary_key=True)
    group_name = models.CharField(verbose_name="人员库名称", max_length=20)
    group_content = models.TextField(verbose_name="人员库描述")

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = "人员库"
        verbose_name_plural = verbose_name
        db_table = 'faces_group'


class FaceData(BaseModel):
    name = models.CharField(verbose_name="真实姓名", max_length=20, primary_key=True)
    sex = models.CharField(verbose_name="性别", choices=(('male', "先生"), ('female', "女士")), max_length=6, null=True)
    content = models.CharField(verbose_name="备注", max_length=100, default="")
    sign = models.TextField(verbose_name="特征值")
    if_local = models.BooleanField(verbose_name="图片是否本地储存", default=True)
    pic = models.ImageField(verbose_name="注册图片", upload_to="media", max_length=2048)
    cos_pic = models.ImageField(verbose_name="COS注册图片", storage=CosStorage(path="facesdata"), max_length=1024,
                                null=True)
    faces_group = models.ForeignKey(verbose_name="人员库", to=FaceGroup, on_delete=models.CASCADE, null=True)

    # pic = models.ImageField(verbose_name="用户特征影响", storage=CosStorage(path="facedata"), max_length=2048)

    def __str__(self):
        return self.name

    def img_pic(self):
        if self.if_local is True:
            return format_html('<img src="/media/{}" style="width:100px;height:auto">', self.pic)
        else:
            return format_html('<img src="{}" style="width:100px;height:auto">', self.cos_pic)

    img_pic.short_description = "注册图片"  # 显示在列表表头的描述

    class Meta:
        verbose_name = "人员数据"
        verbose_name_plural = verbose_name
        db_table = "faces"

    info_html = "<div>{}</div>"

    def group_id(self):
        return format_html(self.info_html, self.faces_group.group_id)

    group_id.short_description = "人员库id"

    def group_name(self):
        return format_html(self.info_html, self.faces_group.group_name)

    group_name.short_description = "人员库名称"

    def group_content(self):
        return format_html(self.info_html, self.faces_group.group_content)

    group_content.short_description = "人员库描述"


class UserFace(BaseModel):
    user = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.CASCADE)
    face = models.ForeignKey(verbose_name="人脸数据", to=FaceData, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "用户 - 人脸"
        verbose_name_plural = verbose_name
        db_table = "user_face"

    def __str__(self):
        return "{}:{}".format(self.user, self.face)

    info_html = "<div>{}</div>"

    def user_username(self):
        return format_html(self.info_html, self.user.username)

    user_username.short_description = "用户名"

    def user_name(self):
        return format_html(self.info_html, self.user.last_name + self.user.first_name)

    user_name.short_description = "姓名"

    def user_age(self):
        return format_html(self.info_html, self.user.age)

    user_age.short_description = "年龄"

    def user_phone(self):
        return format_html(self.info_html, self.user.phone)

    user_phone.short_description = "手机号"

    def user_gender(self):
        if self.user.gender == 'male':
            gender = "先生"
        else:
            gender = "女士"
        return format_html(self.info_html, gender)

    user_gender.short_description = "性别"

    def user_image(self):
        return format_html('<img src="/media/{}" style="width:64px;height:auto">', self.user.image)

    user_image.short_description = "用户头像"

    def face_name(self):
        return format_html(self.info_html, self.face.name)

    face_name.short_description = "真实姓名"

    def face_sex(self):
        if self.face.sex == 'male':
            gender = "先生"
        else:
            gender = "女士"
        return format_html(self.info_html, gender)

    face_sex.short_description = "性别"

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
        return format_html(self.info_html, self.face.faces_group.group_id)

    group_id.short_description = "人员库id"

    def group_name(self):
        return format_html(self.info_html, self.face.faces_group.group_name)

    group_name.short_description = "人员库名称"

    def group_content(self):
        return format_html(self.info_html, self.face.faces_group.group_content)

    group_content.short_description = "人员库描述"
