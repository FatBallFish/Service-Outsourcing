from django.contrib import admin

from apps.passengerFlow.models import PassengerFlow, PassengerFace


# Register your models here.
class PassengerFlowAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("基本信息", {'fields': ('id',)}),
        ("人员信息", {'fields': ('face', 'face_ID', 'face_name', 'face_age', 'face_gender', 'face_sign', 'face_mask')}),
        ("地点信息", {'fields': ('hotel', 'location', 'enter_time', 'exit_time')}),
    )
    readonly_fields = ('id', 'face_ID', 'face_name', 'face_age', 'face_gender', 'face_sign', 'face_mask')

    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = (
        'id', 'face_ID', 'face_name', 'face_age', 'face_gender', 'face_sign', 'face_mask', 'enter_time',
        'exit_time', 'hotel',
        'location')  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('face__ID', 'face__name', 'face__age', 'face__gender', 'face__mask', 'location')  # 列表搜索字段
    list_filter = (
        'face__ID', 'face__name', 'face__age', 'face__gender', 'face__mask', 'enter_time', 'exit_time', 'hotel',
        'location')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class PassengerFaceAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("人员信息", {'fields': ('ID', 'name', 'age', 'gender', 'sign', 'mask')}),
    )
    # readonly_fields = ("id",)
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('ID', 'name', 'age', 'gender', 'sign', 'mask')  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('ID', 'name', 'age', 'gender', 'mask')  # 列表搜索字段
    list_filter = ('ID', 'name', 'age', 'gender', 'mask')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(PassengerFlow, PassengerFlowAdmin)
admin.site.register(PassengerFace, PassengerFaceAdmin)
