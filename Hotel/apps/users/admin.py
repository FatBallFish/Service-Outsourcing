from django.contrib import admin
from django.utils.html import format_html

from apps.users.models import Users


# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基本信息",
         {'fields': (
             'id', 'username', 'nickname', 'email', 'phone', 'read_img_big')}),
        ("权限信息", {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ("隐私&安全信息", {'fields': ('password', 'last_login', 'date_joined')}),
        ("实名认证信息",
         {'fields': ('real_auth', 'auth_ID', 'auth_name', 'auth_gender', 'auth_nation', 'auth_age', 'auth_birthday',
                     'auth_address', 'auth_organization', 'auth_date')}),
        ("人员信息", {'fields': ('face', 'face_name', 'face_gender', 'face_content', 'face_sign', 'face_pic')}),
        ("人员库信息", {'fields': ('group_id', 'group_name', 'group_content')}),
    )
    readonly_fields = (
        'id', 'username', 'password', 'last_login', 'date_joined', 'read_img_big', 'auth_ID', 'auth_name',
        'auth_gender', 'auth_nation', 'auth_age', 'auth_birthday', 'auth_address', 'auth_organization', 'auth_date',
        'face_name', 'face_gender', 'face_content', 'face_sign', 'face_pic', 'group_id', 'group_name',
        'group_content')  # 自定义的数据类型只能设置为只读状态
    # 列表页显示内容
    list_display = ('read_img_small', 'username', "nickname", "email", "phone")
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('username', "nickname", "email", "phone")  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100

    def read_img_big(self, users):
        return format_html('<img src="/media/{}" style="width:100px;height:auto">', users.image)

    read_img_big.short_description = "用户头像"  # 显示在列表表头的描述

    def read_img_small(self, users):
        return format_html('<img src="/media/{}" style="width:32px;height:auto">', users.image)

    read_img_small.short_description = "用户头像"


class AdminSite(admin.AdminSite):
    site_title = "酒店视觉AI"  # 页面显示标题
    site_header = "酒店视觉AI 后台管理"  # 页面头部标题


# admin.site.site_title = "酒店视觉AI 后台管理"
# admin.site.site_header = "酒店视觉AI"

admin.site = AdminSite()

admin.site.register(Users, UsersAdmin)
