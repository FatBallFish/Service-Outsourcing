from datetime import datetime
from django.db import models
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.html import format_html

from extral_apps import MD5
from extral_apps.m_cos import py_cos_main as COS
from Hotel import settings


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


class BaseModel(models.Model):
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)
    update_time = models.DateTimeField(verbose_name="更新时间", default=datetime.now)

    class Meta:
        abstract = True  # 设置为静态表，不会被生成


# Create your models here.
class FaceGroup(BaseModel):
    name = models.CharField(verbose_name="人员库名称", max_length=20, unique=True)
    content = models.TextField(verbose_name="人员库描述", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "人员库"
        verbose_name_plural = verbose_name
        db_table = 'faces_group'


class FaceData(BaseModel):
    ID = models.CharField(verbose_name="身份证ID", max_length=18, primary_key=True)
    name = models.CharField(verbose_name="真实姓名", max_length=20)
    gender = models.CharField(verbose_name="性别", choices=(('male', "先生"), ('female', "女士")), max_length=6, blank=True,
                              null=True)
    content = models.CharField(verbose_name="备注", max_length=100, default="")
    sign = models.TextField(verbose_name="特征值")
    if_local = models.BooleanField(verbose_name="图片是否本地储存", default=True)
    pic = models.ImageField(verbose_name="注册图片", upload_to="media", max_length=2048)
    cos_pic = models.ImageField(verbose_name="COS注册图片", storage=CosStorage(path="facesdata"), max_length=1024,
                                blank=True, null=True)
    faces_group = models.ForeignKey(verbose_name="人员库", to=FaceGroup, on_delete=models.CASCADE, blank=True, null=True)

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
        return format_html(self.info_html, self.faces_group.id)

    group_id.short_description = "人员库id"

    def group_name(self):
        return format_html(self.info_html, self.faces_group.name)

    group_name.short_description = "人员库名称"

    def group_content(self):
        return format_html(self.info_html, self.faces_group.content)

    group_content.short_description = "人员库描述"
