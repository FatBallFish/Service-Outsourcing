from django.contrib import admin
from django.utils.html import format_html

from apps.guests.models import Guests, GuestRoom, Visitor, GuestVisitor


# Register your models here.

class GuestsAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("基本信息", {'fields': ('ID', 'name', 'sex', 'age', 'phone')}),
        ("账号信息",
         {"fields": ("user", 'user_username', 'user_name', 'user_age', 'user_gender', 'user_phone', 'user_image')}),
    )
    radio_fields = {"sex": admin.HORIZONTAL}  # 以单选框形式显示内容，默认为组合框。
    # 参数：垂直布局：admin.VERTICAL  水平布局：admin.HORIZONTAL
    readonly_fields = ('user_username', 'user_name', 'user_age', 'user_gender', 'user_phone', 'user_image')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('ID', 'name', 'sex', 'age', 'phone')  # 列表中显示的字段
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = list_display  # 列表中可点击跳转的字段
    # list_editable = ('content', 'sex', 'faces_group')  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # list_editable = ('faces_group',)  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # 上面那个有点难看，取消

    search_fields = ('ID', 'name', 'phone')  # 列表搜索字段
    list_filter = ('ID', 'name', 'phone')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class GuestRoomAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("来宾信息", {'fields': ('guest', "guest_ID", "guest_name", "guest_sex", "guest_age", "guest_phone")}),
        ("房间信息",
         {"fields": ("room", "room_hotel", "room_floor", "room_number", "room_name", "room_content", "room_type"),
          "classes": ("collaspe", 'wide'),
          "description": "<strong>用户预订的房间信息</strong>"}),
        ("预订信息", {"fields": ('status', 'check_in_time', 'check_out_time'),
                  "description": "<strong>用户预订的房间信息</strong>"})
    )

    readonly_fields = (
        "guest_ID", "guest_name", "guest_sex", "guest_age", "guest_phone", "room_hotel", "room_floor", "room_number",
        "room_name", "room_content", "room_type")
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'guest', 'room_hotel', 'room', 'read_status', 'check_in_time', "check_out_time")  # 列表中显示的字段

    def read_status(self, guestroom):
        if guestroom.status == "booking":
            color = "blue"
            status = "预约中"
        elif guestroom.status == "checkin":
            color = "green"
            status = "已登记入住"
        else:
            color = "red"
            status = "已退房"
        return format_html('<div style="color:{};">{}</div>', color, status)

    read_status.short_description = "入住状态"
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = list_display  # 列表中可点击跳转的字段
    # list_editable = ('content', 'sex', 'faces_group')  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # list_editable = ('faces_group',)  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # 上面那个有点难看，取消

    search_fields = ('guest__ID','guest__name', 'room__hotel', 'room', 'status')  # 列表搜索字段
    list_filter = ('guest__name', 'room__hotel', 'room', 'status', 'check_in_time', 'check_out_time')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class VisitorAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("基本信息", {'fields': ('ID', 'name', 'sex', 'age', 'phone')}),
        ("账号信息",
         {"fields": ("user", 'user_username', 'user_name', 'user_age', 'user_gender', 'user_phone', 'user_image')}),
    )
    radio_fields = {"sex": admin.HORIZONTAL}  # 以单选框形式显示内容，默认为组合框。
    # 参数：垂直布局：admin.VERTICAL  水平布局：admin.HORIZONTAL
    readonly_fields = ('user_username', 'user_name', 'user_age', 'user_gender', 'user_phone', 'user_image')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('ID', 'name', 'sex', 'age', 'phone')  # 列表中显示的字段
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = list_display  # 列表中可点击跳转的字段
    # list_editable = ('content', 'sex', 'faces_group')  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # list_editable = ('faces_group',)  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # 上面那个有点难看，取消

    search_fields = ('ID', 'name', 'phone')  # 列表搜索字段
    list_filter = ('ID', 'name', 'phone')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class GuestVisitorAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("预约基本信息", {'fields': ('guest', 'visitor', 'apply_time', 'visitor_content', 'guest_content', 'status')}),
        ("访客信息", {"fields": ('visitor_ID', 'visitor_name', 'visitor_sex', 'visitor_age', 'visitor_phone')}),
        ("来宾信息", {"fields": ('guest_ID', 'guest_name', 'guest_sex', 'guest_age', 'guest_phone')}),
    )
    readonly_fields = (
        'visitor_ID', 'visitor_name', 'visitor_sex', 'visitor_age', 'visitor_phone', 'guest_ID', 'guest_name',
        'guest_sex',
        'guest_age', 'guest_phone')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'guest', 'visitor', 'apply_time', 'read_status')  # 列表中显示的字段

    def read_status(self, request):
        if request.status == "applying":
            color = "blue"
            status = "申请中"
        elif request.status == "accept":
            color = "green"
            status = "允许访问"
        else:
            color = "red"
            status = "拒绝访问"
        return format_html('<div style="color:{};">{}</div>', color, status)

    list_display_links = list_display  # 列表中可点击跳转的字段
    search_fields = ('guest__name', 'guest__phone', 'visitor__name', 'visitor__phone', 'apply_time', 'status')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(Guests, GuestsAdmin)
admin.site.register(GuestRoom, GuestRoomAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(GuestVisitor, GuestVisitorAdmin)
