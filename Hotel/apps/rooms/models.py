from django.db import models
from django.utils.html import format_html

from apps.users.models import BaseModel
from apps.faces.models import FaceGroup


# Create your models here.
class Hotel(BaseModel):
    name = models.CharField(verbose_name="酒店名称", max_length=100)
    content = models.TextField(verbose_name="备注", blank=True, null=True)
    location = models.TextField(verbose_name="酒店地址")
    imgs = models.TextField(verbose_name="图片集", default="")
    lon = models.CharField(verbose_name="经度", max_length=30, null=True, blank=True)
    lat = models.CharField(verbose_name="纬度", max_length=30, null=True, blank=True)
    province = models.CharField(verbose_name="省份", max_length=20)
    city = models.CharField(verbose_name="城市", max_length=20)
    district = models.CharField(verbose_name="区域", max_length=20)

    class Meta:
        managed = False
        verbose_name = "酒店管理"
        verbose_name_plural = verbose_name
        db_table = "hotels"

    def __str__(self):
        return "{}({})".format(self.name, self.location)


class HotelFaceGroup(BaseModel):
    hotel = models.ForeignKey(verbose_name="酒店", to=Hotel, on_delete=models.CASCADE)
    face_group = models.ForeignKey(verbose_name="人员库", to=FaceGroup, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "酒店 - 人脸库"
        verbose_name_plural = verbose_name
        db_table = "hotel_face_group"

    def __str__(self):
        return "{} - {}".format(self.hotel, self.face_group)

    info_html = "<div>{}</div>"

    def hotel_name(self):
        return format_html(self.info_html, self.hotel.name)

    hotel_name.short_description = "酒店名称"

    def hotel_content(self):
        return format_html(self.info_html, self.hotel.content)

    hotel_content.short_description = "备注"

    def hotel_location(self):
        return format_html(self.info_html, self.hotel.location)

    hotel_location.short_description = "酒店地址"

    def hotel_lon(self):
        return format_html(self.info_html, self.hotel.lon)

    hotel_lon.short_description = "经度"

    def hotel_lat(self):
        return format_html(self.info_html, self.hotel.lat)

    hotel_lat.short_description = "纬度"

    def group_id(self):
        return format_html(self.info_html, self.face_group.group_id)

    group_id.short_description = "人员库id"

    def group_name(self):
        return format_html(self.info_html, self.face_group.group_name)

    group_name.short_description = "人员库名称"

    def group_content(self):
        return format_html(self.info_html, self.face_group.group_content)

    group_content.short_description = "人员库描述"


class Room(BaseModel):
    floor = models.IntegerField(verbose_name="楼层")
    number = models.CharField(verbose_name="房间号", max_length=10)
    name = models.CharField(verbose_name="房间名", max_length=10, blank=True, null=True)
    content = models.TextField(verbose_name="备注", blank=True, null=True)
    room_type_name = models.CharField(verbose_name="房间类型名称", max_length=50, blank=True, null=True)
    room_type_content = models.TextField(verbose_name="房间类型详细描述", blank=True, null=True)
    hotel = models.ForeignKey(verbose_name="酒店", to=Hotel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "房间"
        verbose_name_plural = verbose_name
        db_table = "room"

    def __str__(self):
        return "{}({})".format(self.number, self.name)

    info_html = "<div>{}</div>"

    def hotel_name(self):
        return format_html(self.info_html, self.hotel.name)

    hotel_name.short_description = "酒店名称"

    def hotel_content(self):
        return format_html(self.info_html, self.hotel.content)

    hotel_content.short_description = "备注"

    def hotel_location(self):
        return format_html(self.info_html, self.hotel.location)

    hotel_location.short_description = "酒店地址"

    def hotel_lon(self):
        return format_html(self.info_html, self.hotel.lon)

    hotel_lon.short_description = "经度"

    def hotel_lat(self):
        return format_html(self.info_html, self.hotel.lat)

    hotel_lat.short_description = "纬度"


class Ambitus(models.Model):
    name = models.CharField(verbose_name="周边名称", max_length=30)
    img = models.CharField(verbose_name="周边图片", max_length=500)
    tabs = models.CharField(verbose_name="周边标签", max_length=200)
    lat = models.CharField(verbose_name="周边经度", max_length=30)
    lon = models.CharField(verbose_name="周边纬度", max_length=30)
    city = models.CharField(verbose_name="周边所在城市", max_length=20)

    class Meta:
        verbose_name = "周边"
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'ambitus'

    def __str__(self):
        return self.name

    # def ambitus_img(self):
    #     return format_html('<img src="{}" style="width:100px;height:auto">', self.img)
    # ambitus_img.short_description = "周边图片"