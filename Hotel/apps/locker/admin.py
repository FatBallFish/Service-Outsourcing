from django.contrib import admin

from apps.locker.models import Locker, LockerOrder


# Register your models here.

class LockerAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("使用信息", {'fields': ('id', 'index', 'num', 'available', 'used', 'add_time')}),
        ("所处酒店信息", {"fields": ('hotel', 'hotel_name', 'hotel_content', 'hotel_location', 'hotel_lon', 'hotel_lat')}),
    )
    readonly_fields = (
        'id', 'hotel_name', 'hotel_content', 'hotel_location', 'hotel_lon', 'hotel_lat')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'index', 'num', 'available', 'used', 'add_time')  # 列表中显示的字段

    list_display_links = list_display  # 列表中可点击跳转的字段
    # search_fields = ()  # 列表搜索字段
    list_filter = ('hotel__name', 'index', 'num', 'available', 'used', 'add_time')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class LockerOrderAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("基本信息", {'fields': ('id', 'status', 'add_time', 'expire_time')}),
        ("用户信息", {'fields': ('user', 'user_username', 'user_name', 'user_phone', 'user_image')}),
        ("寄存柜信息", {'fields': ('locker', 'locker_index', 'locker_num', 'locker_available', 'locker_used')}),
        ("所处酒店信息", {"fields": ('hotel_name', 'hotel_content', 'hotel_location', 'hotel_lon', 'hotel_lat')}),
        ("订单信息", {"fields": ('order',)})
    )
    readonly_fields = (
        'id', 'user_username', 'user_name', 'user_phone', 'user_image', 'locker_index', 'locker_num',
        'locker_available', 'locker_used', 'hotel_name', 'hotel_content', 'hotel_location', 'hotel_lon', 'hotel_lat')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'user', 'locker', 'status', 'add_time', 'expire_time', 'order')  # 列表中显示的字段

    list_display_links = list_display  # 列表中可点击跳转的字段
    search_fields = (
        'user__username', 'locker', 'status', 'add_time')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(Locker, LockerAdmin)
admin.site.register(LockerOrder, LockerOrderAdmin)
