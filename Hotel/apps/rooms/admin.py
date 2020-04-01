from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from apps.rooms.resource import RoomResource, HotelResource, AmbitusResource

from apps.rooms.models import Hotel, Room, HotelFaceGroup, Ambitus


# Register your models here.
@admin.register(Hotel)
class HotelAdmin(ImportExportActionModelAdmin):
    # 编辑界面
    fieldsets = (
        ("酒店信息", {'fields': ('name', "content", "location", "imgs", "lon", "lat", "province", "city", "district")}),)
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = (
        'id', 'name', 'content', 'location', 'imgs', "lon", "lat", "province", "city", "district")  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('name', 'content', 'location', "province", "city")  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100
    resource_class = HotelResource


@admin.register(Room)
class RoomAdmin(ImportExportActionModelAdmin):
    # 编辑界面
    fieldsets = (
        ("酒店信息", {'fields': ('hotel', 'hotel_name', 'hotel_content', 'hotel_location', 'hotel_lon', 'hotel_lat')}),
        ("房间基本信息", {'fields': ('floor', "number", "name", "content", "room_type_name", "room_type_content")})
    )
    readonly_fields = ('hotel_name', 'hotel_content', 'hotel_location', 'hotel_lon', 'hotel_lat')

    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = (
        'id', 'hotel', 'floor', 'number', 'name', "content", "room_type_name", "room_type_content")  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('hotel', 'number', 'name', "content", "room_type_name", "room_type_content")  # 列表搜索字段
    list_filter = ('hotel', 'floor', 'number', 'name', "content", "room_type_name", "room_type_content")  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100
    resource_class = RoomResource


@admin.register(HotelFaceGroup)
class HotelFaceGroupAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("酒店信息", {'fields': ('hotel', 'hotel_name', 'hotel_content', 'hotel_location', 'hotel_lon', 'hotel_lat')}),
        ("绑定人员库", {'fields': ('face_group', 'group_id', 'group_name', 'group_content')})
    )
    readonly_fields = (
        'hotel_name', 'hotel_content', 'hotel_location', 'hotel_lon', 'hotel_lat', 'group_id', 'group_name',
        'group_content')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'hotel', 'face_group')  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('hotel', 'face_group__name')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


@admin.register(Ambitus)
class AmbitusAdmin(ImportExportActionModelAdmin):
    # 编辑界面
    fieldsets = (
        ("周边基本信息", {'fields': ('name', 'img', 'tabs')}),
        ("周边位置信息", {'fields': ('lat', 'lon', 'city')})
    )
    # readonly_fields = (,)
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'name', 'tabs', 'lat', 'lon', 'city')  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('name', 'tabs', 'city')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100
    resource_class = AmbitusResource
