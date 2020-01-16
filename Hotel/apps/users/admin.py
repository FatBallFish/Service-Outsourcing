from django.contrib import admin
from django.utils.html import format_html

from apps.users.models import Users


# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基本信息",
         {'fields': (
             'id', 'username', 'first_name', 'last_name', 'nickname', 'email', 'phone', 'gender', 'read_img_big')}),
        ("权限信息", {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ("隐私&安全信息", {'fields': ('password', 'last_login', 'date_joined')})
    )
    radio_fields = {"gender": admin.HORIZONTAL}  # 以单选框形式显示内容，默认为组合框。
    # 参数：垂直布局：admin.VERTICAL  水平布局：admin.HORIZONTAL
    readonly_fields = ('id', 'username', 'password', 'last_login', 'date_joined', 'read_img_big')  # 自定义的数据类型只能设置为只读状态
    # 列表页显示内容
    list_display = ('read_img_small', 'username', 'first_name', 'last_name', "nickname", "email", "phone")
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('username', 'first_name', 'last_name', "nickname", "email", "phone")  # 列表搜索字段
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
