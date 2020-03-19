from django.db import models
from django.utils.html import format_html

from apps.users.models import Users, BaseModel
from apps.rooms.models import Hotel, Room
from apps.realauth.models import RealAuth
from datetime import datetime


# Create your models here.
class Guests(BaseModel):
    # todo room 外键
    user = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.SET_NULL, blank=True, null=True)
    real_auth = models.ForeignKey(verbose_name="实名认证库", to=RealAuth, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "来宾"
        verbose_name_plural = verbose_name
        db_table = "guests"

    def __str__(self):
        return "{}({})".format(self.real_auth.name, self.real_auth.gender)

    info_html = "<div>{}</div>"

    def user_username(self):
        return format_html(self.info_html, self.user.username)

    user_username.short_description = "用户名"

    def user_name(self):
        return format_html(self.info_html, self.user.last_name + self.user.first_name)

    user_name.short_description = "姓名"

    def user_nickname(self):
        return format_html(self.info_html, self.user.nickname)

    user_nickname.short_description = "昵称"

    def user_phone(self):
        return format_html(self.info_html, self.user.phone)

    user_phone.short_description = "手机号"

    def user_image(self):
        return format_html('<img src="/api/pic/get/users?name={}" style="width:64px;height:auto">', self.user.username)

    user_image.short_description = "用户头像"

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


class Orders(BaseModel):
    hotel = models.ForeignKey(verbose_name="酒店", to=Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(verbose_name="房间", to=Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(verbose_name="预订人", to=Guests, on_delete=models.CASCADE)
    days = models.IntegerField(verbose_name="预订天数")
    price = models.FloatField(verbose_name="单价")
    totalprice = models.FloatField(verbose_name="总价")
    date_start = models.DateTimeField(verbose_name="开始时间")
    date_end = models.DateTimeField(verbose_name="结束时间")
    guests = models.TextField(verbose_name="住客", default="")
    status = models.IntegerField(verbose_name="订单状态", default=0)
    pay_time = models.DateTimeField(verbose_name="支付时间")

    class Meta:
        managed = False
        verbose_name = "订单"
        verbose_name_plural = verbose_name
        db_table = "orders"

    def __str__(self):
        return "{}".format(self.id)


class GuestRoom(models.Model):
    guest = models.ForeignKey(verbose_name="来宾", to=Guests, on_delete=models.CASCADE)
    room = models.ForeignKey(verbose_name="入住房间", to=Room, on_delete=models.CASCADE)
    status = models.CharField(verbose_name="入住状态",
                              choices=(("booking", "预订中"), ("checkin", "已登记入住"), ("checkout", "已退房")), max_length=8,
                              default="booking")
    check_in_time = models.DateTimeField(verbose_name="入住时间", default=datetime.now)
    check_out_time = models.DateTimeField(verbose_name="退房时间", blank=True, null=True)
    order = models.ForeignKey(verbose_name="订单", to=Orders, on_delete=models.CASCADE, null=True)
    name = models.CharField(verbose_name="标题", max_length=30)
    if_locker = models.IntegerField(verbose_name="是否预订寄存柜",blank=True, null=True)

    class Meta:
        managed = False
        verbose_name = "来宾-房间"
        verbose_name_plural = verbose_name
        db_table = "guest_room"

    def __str__(self):
        return "{}-{}({})".format(self.guest.real_auth.name, self.room.name, self.status)

    def guest_ID(self):
        return format_html('<div>{}</div>', self.guest.real_auth.ID)

    guest_ID.short_description = "身份证号"

    def guest_name(self):
        return format_html('<div>{}</div>', self.guest.real_auth.name)

    guest_name.short_description = "姓名"

    def guest_nation(self):
        return format_html('<div>{}</div>', self.guest.real_auth.nation)

    guest_nation.short_description = "民族"

    def guest_birthday(self):
        return format_html('<div>{}</div>', self.guest.real_auth.birthday)

    guest_birthday.short_description = "出生年月"

    def guest_address(self):
        return format_html('<div>{}</div>', self.guest.real_auth.address)

    guest_address.short_description = "住址"

    def guest_age(self):
        today = datetime.now().date()
        differ = (today - self.guest.real_auth.birthday) // 365
        differ = differ.days
        return format_html('<div>{}</div>', differ)

    guest_age.short_description = "年龄"

    def guest_gender(self):
        if self.guest.real_auth.gender == "male":
            gender = "先生"
        else:
            gender = "女士"
        return format_html('<div>{}</div>', gender)

    guest_gender.short_description = "性别"

    def guest_phone(self):
        return format_html('<div>{}</div>', self.guest.user.phone)

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
    user = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.SET_NULL, blank=True, null=True)
    real_auth = models.ForeignKey(verbose_name="实名认证库", to=RealAuth, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "访客"
        verbose_name_plural = verbose_name
        db_table = "visitors"

    def __str__(self):
        return "{}({})".format(self.real_auth.name, self.real_auth.gender)

    info_html = "<div>{}</div>"

    def user_username(self):
        return format_html(self.info_html, self.user.username)

    user_username.short_description = "用户名"

    def user_name(self):
        return format_html(self.info_html, self.user.last_name + self.user.first_name)

    user_name.short_description = "姓名"

    def user_nickname(self):
        return format_html(self.info_html, self.user.nickname)

    user_nickname.short_description = "昵称"

    def user_phone(self):
        return format_html(self.info_html, self.user.phone)

    user_phone.short_description = "手机号"

    def user_image(self):
        return format_html('<img src="/api/pic/get/users?name={}" style="width:64px;height:auto">', self.user.username)

    user_image.short_description = "用户头像"

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


class GuestVisitor(models.Model):
    guest = models.ForeignKey(verbose_name="来宾", to=Guests, on_delete=models.CASCADE)
    visitor = models.ForeignKey(verbose_name="访客", to=Visitor, on_delete=models.CASCADE)
    apply_time = models.DateTimeField(verbose_name="申请时间", default=datetime.now)
    status = models.CharField(verbose_name="申请状态",
                              choices=(("applying", "申请中"), ("accept", "允许访问"), ("refuse", "拒绝访问")), default="applying",
                              max_length=8)
    visitor_content = models.TextField(verbose_name="访客申请内容", blank=True, null=True)
    guest_content = models.TextField(verbose_name="来宾回复内容", blank=True, null=True)
    start_time = models.DateTimeField(verbose_name="开始时间", blank=True, null=True)
    end_time = models.DateTimeField(verbose_name="结束时间", blank=True, null=True)
    room = models.ForeignKey(verbose_name="访问房间", to=Room, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        verbose_name = "访客申请记录"
        verbose_name_plural = verbose_name
        db_table = "guest_visitor"

    def __str__(self):
        return "{} visit {}({})".format(self.visitor, self.guest, self.apply_time)

    info_html = "<div>{}</div>"

    def guest_ID(self):
        return format_html('<div>{}</div>', self.guest.real_auth.ID)

    guest_ID.short_description = "身份证号"

    def guest_name(self):
        return format_html('<div>{}</div>', self.guest.real_auth.name)

    guest_name.short_description = "姓名"

    def guest_nation(self):
        return format_html('<div>{}</div>', self.guest.real_auth.nation)

    guest_nation.short_description = "民族"

    def guest_birthday(self):
        return format_html('<div>{}</div>', self.guest.real_auth.birthday)

    guest_birthday.short_description = "出生年月"

    def guest_address(self):
        return format_html('<div>{}</div>', self.guest.real_auth.address)

    guest_address.short_description = "住址"

    def guest_age(self):
        today = datetime.now().date()
        year = (today - self.guest.real_auth.birthday) // 365
        year = year.days
        return format_html('<div>{}</div>', year)

    guest_age.short_description = "年龄"

    def guest_gender(self):
        if self.guest.real_auth.gender == "male":
            gender = "先生"
        else:
            gender = "女士"
        return format_html('<div>{}</div>', gender)

    guest_gender.short_description = "性别"

    def guest_phone(self):
        return format_html('<div>{}</div>', self.guest.user.phone)

    guest_phone.short_description = "手机号"

    def visitor_ID(self):
        return format_html(self.info_html, self.visitor.real_auth.ID)

    visitor_ID.short_description = "身份证号"

    def visitor_name(self):
        return format_html(self.info_html, self.visitor.real_auth.name)

    visitor_name.short_description = "姓名"

    def visitor_nation(self):
        return format_html('<div>{}</div>', self.visitor.real_auth.nation)

    visitor_nation.short_description = "民族"

    def visitor_birthday(self):
        return format_html('<div>{}</div>', self.visitor.real_auth.birthday)

    visitor_birthday.short_description = "出生年月"

    def visitor_address(self):
        return format_html('<div>{}</div>', self.visitor.real_auth.address)

    visitor_address.short_description = "住址"

    def visitor_age(self):
        today = datetime.now().date()
        year = (today - self.visitor.real_auth.birthday) // 365
        year = year.days
        return format_html('<div>{}</div>', year)

    visitor_age.short_description = "年龄"

    def visitor_gender(self):
        if self.visitor.real_auth.gender == 'male':
            gender = "先生"
        else:
            gender = "女士"
        return format_html(self.info_html, gender)

    visitor_gender.short_description = "性别"

    def visitor_phone(self):
        return format_html(self.info_html, self.visitor.user.phone)

    visitor_phone.short_description = "手机号"
