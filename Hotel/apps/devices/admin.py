from django.contrib import admin
from apps.devices.models import Device, DeviceGroup, DeviceUser


# Register your models here.

class DeviceAdmin(admin.ModelAdmin):
    fieldsets = (
        ("设备信息", {'fields': ('device_id', 'device_name', 'device_content')}),
    )
    # readonly_fields = ('device_id', 'device_name', 'device_content')
    # 列表页显示内容
    list_display = ('device_id', 'device_name', 'device_content')
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('device_id', 'device_name', 'device_content')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class DeviceGroupAdmin(admin.ModelAdmin):
    fieldsets = (
        ("设备-人员库绑定信息", {'fields': ('device', 'faces_group')}),
    )
    # readonly_fields = ('device',)  # 自定义的数据类型只能设置为只读状态
    # 列表页显示内容
    list_display = ('device', 'faces_group')
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('device__device_name', 'faces_group__name')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class DeviceUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("设备-用户绑定信息", {'fields': ('device', 'user')}),
    )
    # readonly_fields = ('device',)
    # 列表页显示内容
    list_display = ('device', 'user')
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('device__device_name', 'user__username')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceGroup, DeviceGroupAdmin)
admin.site.register(DeviceUser, DeviceUserAdmin)
