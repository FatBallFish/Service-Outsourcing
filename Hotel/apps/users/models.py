from datetime import datetime
from django.db import models
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
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
class FaceData(BaseModel):
    realname = models.CharField(verbose_name="真实姓名", max_length=20, primary_key=True)
    sign = models.CharField(verbose_name="用户特征", max_length=2048)
    pic = models.ImageField(verbose_name="用户特征影响", upload_to="media/", max_length=2048)
    # pic = models.ImageField(verbose_name="用户特征影响", storage=CosStorage(path="facedata"), max_length=2048)

    def __str__(self):
        return self.realname

    class Meta:
        verbose_name = "人脸数据库"
        verbose_name_plural = verbose_name
        db_table = "faces"
