from django.contrib import admin
from apps.rooms.models import Hotel, Room, HotelFaceGroup


# Register your models here.
class HotelAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("酒店信息", {'fields': ('name', "content", "location")}),)
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'name', 'content', 'location')  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('name', 'content', 'location')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class RoomAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("酒店信息", {'fields': ('hotel', 'hotel_name', 'hotel_content', 'hotel_location')}),
        ("房间基本信息", {'fields': ('floor', "number", "name", "content", "room_type_name", "room_type_content")})
    )
    readonly_fields = ('hotel_name', 'hotel_content', 'hotel_location')

    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = (
        'id', 'hotel', 'floor', 'number', 'name', "content", "room_type_name", "room_type_content")  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('hotel', 'number', 'name', "content", "room_type_name", "room_type_content")  # 列表搜索字段
    list_filter = ('hotel', 'floor', 'number', 'name', "content", "room_type_name", "room_type_content")  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class HotelFaceGroupAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("酒店信息", {'fields': ('hotel', 'hotel_name', 'hotel_content', 'hotel_location')}),
        ("绑定人员库", {'fields': ('face_group', 'group_id', 'group_name', 'group_content')})
    )
    readonly_fields = ('hotel_name', 'hotel_content', 'hotel_location', 'group_id', 'group_name', 'group_content')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'hotel', 'face_group')  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('hotel', 'face_group__group_name')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(HotelFaceGroup, HotelFaceGroupAdmin)
