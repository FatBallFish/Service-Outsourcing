from django.db import models
from django.utils.html import format_html

from apps.users.models import BaseModel, Users
from apps.rooms.models import Hotel
from apps.guests.models import Orders

from datetime import datetime


# Create your models here.
class Locker(BaseModel):
    index = models.IntegerField(verbose_name="单元序列")
    num = models.IntegerField(verbose_name="编号")
    hotel = models.ForeignKey(verbose_name="所处酒店", to=Hotel, on_delete=models.CASCADE)
    available = models.BooleanField(verbose_name="是否可用", default=True)
    used = models.BooleanField(verbose_name="是否被使用", default=False)

    class Meta:
        verbose_name = "寄存柜信息"
        verbose_name_plural = verbose_name
        db_table = "locker"

    def __str__(self):
        return "{}柜{}号({})".format(self.index, self.num, self.hotel.name)

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


status_choice = (("applying", "预约中"), ("using", "使用中"), ("canceled", "被取消"), ("done", "使用完成"))


class LockerOrder(BaseModel):
    user = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.CASCADE)
    locker = models.ForeignKey(verbose_name="寄存柜信息", to=Locker, on_delete=models.CASCADE)
    status = models.CharField(verbose_name="使用状态", max_length=50, choices=status_choice)
    expire_time = models.DateTimeField(verbose_name="过期时间", default=datetime.now)
    order = models.ForeignKey(verbose_name="订单信息", to=Orders, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "寄存柜使用情况"
        verbose_name_plural = verbose_name
        db_table = "locker_order"

    def __str__(self):
        return "{} - {}".format(self.user, self.locker)

    info_html = "<div>{}</div>"

    def user_username(self):
        return format_html(self.info_html, self.user.username)

    user_username.short_description = "用户名"

    def user_name(self):
        return format_html(self.info_html, self.user.last_name + self.user.first_name)

    user_name.short_description = "姓名"

    def user_phone(self):
        return format_html(self.info_html, self.user.phone)

    user_phone.short_description = "手机号"

    def user_image(self):
        return format_html('<img src="/api/pic/get/users?name={}" style="width:64px;height:auto">', self.user.username)

    user_image.short_description = "用户头像"

    def locker_index(self):
        return format_html(self.info_html, self.locker.index)

    locker_index.short_description = "单元序列"

    def locker_num(self):
        return format_html(self.info_html, self.locker.num)

    locker_num.short_description = "柜子编号"

    def locker_available(self):
        return format_html(self.info_html, self.locker.available)

    locker_available.short_description = "可用状态"

    def locker_used(self):
        return format_html(self.info_html, self.locker.used)

    locker_used.short_description = "使用状态"

    def hotel_name(self):
        return format_html(self.info_html, self.locker.hotel.name)

    hotel_name.short_description = "酒店名称"

    def hotel_content(self):
        return format_html(self.info_html, self.locker.hotel.content)

    hotel_content.short_description = "备注"

    def hotel_location(self):
        return format_html(self.info_html, self.locker.hotel.location)

    hotel_location.short_description = "酒店地址"

    def hotel_lon(self):
        return format_html(self.info_html, self.locker.hotel.lon)

    hotel_lon.short_description = "经度"

    def hotel_lat(self):
        return format_html(self.info_html, self.locker.hotel.lat)

    hotel_lat.short_description = "纬度"
