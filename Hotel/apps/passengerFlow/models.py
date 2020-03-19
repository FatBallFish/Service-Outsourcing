from django.db import models
from datetime import datetime
from django.utils.html import format_html

from apps.rooms.models import Hotel
from apps.users.models import BaseModel

# Create your models here.
gender_choice = (("male", "先生"), ("female", "女士"), ("unknown", "未知"))


class PassengerFace(BaseModel):
    ID = models.CharField(verbose_name="ID", max_length=18, primary_key=True)
    name = models.CharField(verbose_name="姓名", max_length=20)
    age = models.IntegerField(verbose_name="年龄")
    gender = models.CharField(verbose_name="性别", choices=gender_choice, max_length=7, blank=True, null=True)
    sign = models.TextField(verbose_name="特征值")
    mask = models.BooleanField(verbose_name="脸部遮罩物", null=True, blank=True)
    num = models.IntegerField(verbose_name="出现次数", default=0)

    class Meta:
        verbose_name = "客流人脸"
        verbose_name_plural = verbose_name
        db_table = "passenger_face"

    def __str__(self):
        return "({}){}".format(self.name, self.ID)


class PassengerFlow(models.Model):
    face = models.ForeignKey(verbose_name="客流人脸信息", to=PassengerFace, on_delete=models.CASCADE)
    enter_time = models.DateTimeField(verbose_name="进入时间", default=datetime.now)
    exit_time = models.DateTimeField(verbose_name="离开时间", null=True, blank=True)
    hotel = models.ForeignKey(verbose_name="记录酒店", to=Hotel, on_delete=models.CASCADE)
    location = models.CharField(verbose_name="记录地点", max_length=300, default="", null=True, blank=True)

    class Meta:
        verbose_name = "客流量"
        verbose_name_plural = verbose_name
        db_table = "passenger_flow"

    def __str__(self):
        return "{}()".format(self.face, self.location)

    info_html = "<div>{}</div>"

    def face_ID(self):
        return format_html(self.info_html, self.face.ID)

    face_ID.short_description = "人脸ID"

    def face_name(self):
        return format_html(self.info_html, self.face.name)

    face_name.short_description = "姓名"

    def face_gender(self):
        if self.face.gender == 'male':
            gender = "先生"
        elif self.face.gender == "female":
            gender = "女士"
        else:
            gender = "未知"
        return format_html(self.info_html, gender)

    face_gender.short_description = "性别"

    def face_age(self):
        return format_html(self.info_html, self.face.age)

    face_age.short_description = "年龄"

    def face_sign(self):
        return format_html(self.info_html, self.face.sign)

    face_sign.short_description = "特征值"

    def face_mask(self):
        return format_html(self.info_html, self.face.mask)

    face_mask.short_description = "是否有嘴部遮罩物"
