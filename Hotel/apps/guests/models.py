from django.db import models
from django.utils.html import format_html

from apps.users.models import Users, BaseModel
from apps.rooms.models import Hotel, Room
from datetime import datetime


# Create your models here.
class Guests(BaseModel):
    ID = models.CharField(verbose_name="身份证号", max_length=18, primary_key=True)
    name = models.CharField(verbose_name="姓名", max_length=30)
    age = models.IntegerField(verbose_name="年龄")
    sex = models.CharField(verbose_name="性别", choices=(('male', "先生"), ('female', "女士")), max_length=6)
    phone = models.CharField(verbose_name="手机号", max_length=11, null=True)
    # todo room 外键
    user = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "来宾"
        verbose_name_plural = verbose_name
        db_table = "guests"

    def __str__(self):
        return "{}({})".format(self.name, self.sex)

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


class GuestRoom(models.Model):
    guest = models.ForeignKey(verbose_name="来宾", to=Guests, on_delete=models.CASCADE)
    room = models.ForeignKey(verbose_name="入住房间", to=Room, on_delete=models.CASCADE)
    status = models.CharField(verbose_name="入住状态",
                              choices=(("booking", "预订中"), ("checkin", "已登记入住"), ("checkout", "已退房")), max_length=8,
                              default="booking")
    check_in_time = models.DateTimeField(verbose_name="入住时间", default=datetime.now)
    check_out_time = models.DateTimeField(verbose_name="退房时间", null=True)

    class Meta:
        verbose_name = "来宾-房间"
        verbose_name_plural = verbose_name
        db_table = "guest_room"

    def __str__(self):
        return "{}-{}({})".format(self.guest.name, self.room.name, self.status)

    def guest_ID(self):
        return format_html('<div>{}</div>', self.guest.ID)

    guest_ID.short_description = "身份证号"

    def guest_name(self):
        return format_html('<div>{}</div>', self.guest.name)

    guest_name.short_description = "姓名"

    def guest_age(self):
        return format_html('<div>{}</div>', self.guest.age)

    guest_age.short_description = "年龄"

    def guest_sex(self):
        if self.guest.sex == "male":
            sex = "先生"
        else:
            sex = "女士"
        return format_html('<div>{}</div>', sex)

    guest_sex.short_description = "性别"

    def guest_phone(self):
        return format_html('<div>{}</div>', self.guest.phone)

    guest_phone.short_description = "手机号"

    def room_floor(self):
        return format_html('<div>{}</div>', self.room.floor)

    room_floor.short_description = "楼层"

    def room_number(self):
        return format_html('<div>{}</div>', self.room.number)

    room_number.short_description = "房间号"

    def room_name(self):
        return format_html('<div>{}</div>', self.room.name)

    room_name.short_description = "房间名"

    def room_content(self):
        return format_html('<div>{}</div>', self.room.content)

    room_content.short_description = "备注"

    def room_type(self):
        return format_html('<div>{}</div>', self.room.room_type_name)

    room_type.short_description = "房间类型"

    def room_hotel(self):
        return format_html('<div>{}</div>', self.room.hotel)

    room_hotel.short_description = "所处酒店"


class Visitor(BaseModel):
    ID = models.CharField(verbose_name="身份证号", max_length=18, primary_key=True)
    name = models.CharField(verbose_name="姓名", max_length=30)
    age = models.IntegerField(verbose_name="年龄")
    sex = models.CharField(verbose_name="性别", choices=(('male', "先生"), ('female', "女士")), max_length=6)
    phone = models.CharField(verbose_name="手机号", max_length=11, null=True)
    # todo room 外键
    user = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "访客"
        verbose_name_plural = verbose_name
        db_table = "visitors"

    def __str__(self):
        return "{}({})".format(self.name, self.sex)

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


class GuestVisitor(models.Model):
    guest = models.ForeignKey(verbose_name="来宾", to=Guests, on_delete=models.CASCADE)
    visitor = models.ForeignKey(verbose_name="访客", to=Visitor, on_delete=models.CASCADE)
    apply_time = models.DateTimeField(verbose_name="申请时间", default=datetime.now)
    status = models.CharField(verbose_name="申请状态",
                              choices=(("applying", "申请中"), ("accept", "允许访问"), ("refuse", "拒绝访问")), default="applying",
                              max_length=8)
    visitor_content = models.TextField(verbose_name="访客申请内容", null=True)
    guest_content = models.TextField(verbose_name="来宾回复内容", null=True)

    class Meta:
        verbose_name = "访客申请记录"
        verbose_name_plural = verbose_name
        db_table = "guest_visitor"

    def __str__(self):
        return "{} visit {}({})".format(self.visitor, self.guest, self.apply_time)

    info_html = "<div>{}</div>"

    def guest_ID(self):
        return format_html(self.info_html, self.guest.ID)

    guest_ID.short_description = "身份证号"

    def guest_name(self):
        return format_html(self.info_html, self.guest.name)

    guest_name.short_description = "姓名"

    def guest_age(self):
        return format_html(self.info_html, self.guest.age)

    guest_age.short_description = "年龄"

    def guest_sex(self):
        if self.guest.sex == 'male':
            gender = "先生"
        else:
            gender = "女士"
        return format_html(self.info_html, gender)

    guest_sex.short_description = "性别"

    def guest_phone(self):
        return format_html(self.info_html, self.guest.phone)

    guest_phone.short_description = "手机号"

    def visitor_ID(self):
        return format_html(self.info_html, self.visitor.ID)

    visitor_ID.short_description = "身份证号"

    def visitor_name(self):
        return format_html(self.info_html, self.visitor.name)

    visitor_name.short_description = "姓名"

    def visitor_age(self):
        return format_html(self.info_html, self.visitor.age)

    visitor_age.short_description = "年龄"

    def visitor_sex(self):
        if self.visitor.sex == 'male':
            gender = "先生"
        else:
            gender = "女士"
        return format_html(self.info_html, gender)

    visitor_sex.short_description = "性别"

    def visitor_phone(self):
        return format_html(self.info_html, self.visitor.phone)

    visitor_phone.short_description = "手机号"

