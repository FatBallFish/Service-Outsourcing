from django.db import models
from django.utils.html import format_html
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from Hotel import settings
from apps.users.models import BaseModel

from extral_apps import MD5
from extral_apps.m_cos import py_cos_main as COS


# Create your models here.
@deconstructible
class CosStorage(Storage):
    path = ""

    def __init__(self, path: str = ""):
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

    # def delete(self, name):
    #     try:
    #         COS.del_file()

    def url(self, name):
        return name


class PicBed(BaseModel):
    name = models.CharField(verbose_name="图片名称", max_length=200)
    upload_to = models.TextField(verbose_name="上传到", default="/")
    content = models.TextField(verbose_name="描述", default="", null=True, blank=True)
    md5 = models.CharField(verbose_name="MD5", max_length=32, default="", null=True, blank=True)
    if_local = models.BooleanField(verbose_name="是否本地存储", default=False)
    local_url = models.ImageField(verbose_name="本地存储地址", upload_to="media", max_length=2048, null=True, blank=True)
    cos_url = models.ImageField(verbose_name="COS存储地址", storage=CosStorage(""), max_length=2048, null=True, blank=True)

    class Meta:
        verbose_name = "图床"
        verbose_name_plural = verbose_name
        db_table = "picbed"

    def __str__(self):
        return self.name

    def img_pic(self):
        if self.if_local is True:
            return format_html('<img src="/media/{}" style="width:100px;height:auto">', self.local_url)
        else:
            return format_html('<img src="{}" style="width:100px;height:auto">', self.cos_url)

    img_pic.short_description = "图片"
