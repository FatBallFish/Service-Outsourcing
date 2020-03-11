from django.contrib import admin
from django.utils.html import format_html

from apps.guests.models import Guests, GuestRoom, Visitor, GuestVisitor, Orders


# Register your models here.
# todo 全部重改
class GuestsAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("实名信息", {'fields': (
            'real_auth', 'auth_ID', 'auth_name', 'auth_gender', 'auth_nation', 'auth_age', 'auth_birthday',
            'auth_address',
            'auth_organization', 'auth_date')}),
        ("绑定账号信息",
         {"fields": ("user", 'user_username', 'user_nickname', 'user_phone', 'user_image')}),
    )
    readonly_fields = (
        'auth_ID', 'auth_name', 'auth_gender', 'auth_nation', 'auth_age', 'auth_birthday', 'auth_address',
        'auth_organization', 'auth_date', 'user_username', 'user_nickname', 'user_phone', 'user_image')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('auth_name', 'auth_gender', 'auth_age', 'auth_nation', 'user')  # 列表中显示的字段
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = list_display  # 列表中可点击跳转的字段
    # list_editable = ('content', 'sex', 'faces_group')  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # list_editable = ('faces_group',)  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # 上面那个有点难看，取消

    search_fields = ('real_auth__ID', 'real_auth__name', 'auth_address', 'user__phone')  # 列表搜索字段
    list_filter = (
        'real_auth__ID', 'real_auth__name', 'real_auth__gender', 'real_auth__birthday', 'user__phone')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class GuestRoomAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("来宾信息", {'fields': ('guest', "guest_ID", "guest_name", "guest_gender", "guest_age", "guest_phone")}),
        ("房间信息",
         {"fields": ("room", "room_hotel", "room_floor", "room_number", "room_name", "room_content", "room_type"),
          "classes": ("collaspe", 'wide'),
          "description": "<strong>用户预订的房间信息</strong>"}),
        ("预订信息", {"fields": ('status', 'check_in_time', 'check_out_time'),
                  "description": "<strong>用户预订的房间信息</strong>"}),
        ("订单信息", {'fields': ('name', 'order')})
    )

    readonly_fields = (
        "guest_ID", "guest_name", "guest_gender", "guest_age", "guest_phone", "room_hotel", "room_floor", "room_number",
        "room_name", "room_content", "room_type")
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = (
        'id', 'guest', 'room_hotel', 'room', 'read_status', 'check_in_time', "check_out_time", 'name',
        'order')  # 列表中显示的字段

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

    search_fields = ('guest__real_auth__ID', 'guest__real_auth__name', 'room__hotel', 'room', 'status')  # 列表搜索字段
    list_filter = (
        'guest__real_auth__name', 'room__hotel', 'room', 'status', 'check_in_time', 'check_out_time')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class VisitorAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("实名信息", {'fields': (
            'real_auth', 'auth_ID', 'auth_name', 'auth_gender', 'auth_nation', 'auth_age', 'auth_birthday',
            'auth_address', 'auth_organization', 'auth_date')}),
        ("绑定账号信息",
         {"fields": ("user", 'user_username', 'user_nickname', 'user_phone', 'user_image')}),
    )
    readonly_fields = (
        'auth_ID', 'auth_name', 'auth_gender', 'auth_nation', 'auth_age', 'auth_birthday', 'auth_address',
        'auth_organization', 'auth_date', 'user_username', 'user_nickname', 'user_phone', 'user_image')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('auth_name', 'auth_gender', 'auth_age', 'auth_nation', 'user')  # 列表中显示的字段
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = list_display  # 列表中可点击跳转的字段
    # list_editable = ('content', 'sex', 'faces_group')  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # list_editable = ('faces_group',)  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # 上面那个有点难看，取消

    search_fields = ('real_auth__ID', 'real_auth__name', 'auth_address', 'user__phone')  # 列表搜索字段
    list_filter = (
        'real_auth__ID', 'real_auth__name', 'real_auth__gender', 'real_auth__birthday', 'user__phone')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class GuestVisitorAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("预约基本信息", {'fields': (
            'guest', 'visitor', 'apply_time', 'visitor_content', 'guest_content', 'status', 'start_time', 'end_time')}),
        ("访客信息", {"fields": ('visitor_ID', 'visitor_name', 'visitor_gender', 'visitor_age', 'visitor_phone')}),
        ("来宾信息", {"fields": ('guest_ID', 'guest_name', 'guest_gender', 'guest_age', 'guest_phone')}),
    )
    readonly_fields = (
        'visitor_ID', 'visitor_name', 'visitor_gender', 'visitor_age', 'visitor_phone', 'guest_ID', 'guest_name',
        'guest_gender', 'guest_age', 'guest_phone')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'guest', 'visitor', 'apply_time', 'read_status', 'start_time', 'end_time')  # 列表中显示的字段

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

    read_status.short_description = "申请状态"

    list_display_links = list_display  # 列表中可点击跳转的字段
    search_fields = (
        'guest__real_auth__name', 'guest__user__phone', 'visitor__real_auth__name', 'visitor__user__phone',
        'apply_time',
        'status')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class OrderAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("订单基本信息",
         {'fields': (
             'id', 'status', 'guest', 'guests', 'date_start', 'date_end', 'days', 'price', 'totalprice', 'add_time',
             'update_time',
             'pay_time')}),
        ("酒店信息", {"fields": ('hotel', 'room')}),
    )
    readonly_fields = ('id',)
    # readonly_fields = (
    #     'visitor_ID', 'visitor_name', 'visitor_gender', 'visitor_age', 'visitor_phone', 'guest_ID', 'guest_name',
    #     'guest_gender', 'guest_age', 'guest_phone')
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('id', 'guest', 'add_time', 'price', 'totalprice', 'read_status')  # 列表中显示的字段

    def read_status(self, request):
        if request.status == 0:
            color = "red"
            status = "未支付"
        elif request.status == 1:
            color = "orange"
            status = "已预订"
        elif request.status == 2:
            color = "blue"
            status = "入住中"
        elif request.status == 3:
            color = "gray"
            status = "已退房"
        else:
            color = "red"
            status = "其他状态"
        return format_html('<div style="color:{};">{}</div>', color, status)

    read_status.short_description = "订单状态"

    list_display_links = list_display  # 列表中可点击跳转的字段
    search_fields = (
        'id', 'guest__real_auth__name', 'guest__user__phone', 'guests',
        'add_time', 'pay_time',
        'status')  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(Guests, GuestsAdmin)
admin.site.register(GuestRoom, GuestRoomAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(GuestVisitor, GuestVisitorAdmin)
admin.site.register(Orders, OrderAdmin)
