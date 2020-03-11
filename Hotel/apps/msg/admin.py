from django.contrib import admin
from apps.msg.models import Messages, MessageText, MessageSysStatus


# Register your models here.
class MessageTextAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ('id', 'title', 'content', 'add_time', 'update_time')}),
    )
    readonly_fields = ('id',)  # 自定义的数据类型只能设置为只读状态
    # 列表页显示内容
    list_display = ('id', 'title', "content", 'add_time')
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('title', "content")  # 列表搜索字段
    list_filter = search_fields  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class MessagesAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ('id', 'sendID', 'recID', 'type', 'subtype', 'add_time', 'update_time', 'extra')}),
        ("消息内容", {'fields': ('text', 'text_id', 'text_title', 'text_content', 'text_add_time', 'text_update_time')}),
        ("读取状态", {'fields': ('status',)})
    )
    readonly_fields = (
        'id', 'text_id', 'text_title', 'text_content', 'text_add_time', 'text_update_time')  # 自定义的数据类型只能设置为只读状态
    # 列表页显示内容
    list_display = ('id', 'sendID', 'recID', 'type', 'subtype', 'text', 'extra', "status", 'add_time')
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('sendID__username', 'recID__username', 'text__title', 'text__content', 'extra')  # 列表搜索字段
    list_filter = ('id', 'sendID__username', 'recID__username', 'type', 'subtype', 'status')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class MessageSysStatusAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ('id', 'add_time', 'update_time')}),
        ("消息内容", {'fields': (
            'message', 'message_id', 'message_type', 'message_subtype', 'text_title', 'text_content', 'message_extra',
            'message_add_time', 'message_update_time')}),
        ("读取状态", {'fields': ('recID', 'status',)})
    )
    readonly_fields = (
        'id', 'message_id', 'message_type', 'message_subtype', 'text_title', 'text_content', 'message_add_time',
        'message_extra', 'message_update_time')  # 自定义的数据类型只能设置为只读状态
    # 列表页显示内容
    list_display = ('id', 'message', "status", 'add_time')
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('message__text__title', 'message__title__content', 'message__extra')  # 列表搜索字段
    list_filter = (
        'id', 'message__type', 'message__subtype', 'message__text__title', 'message__text__content', 'status')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(Messages, MessagesAdmin)
admin.site.register(MessageText, MessageTextAdmin)
admin.site.register(MessageSysStatus, MessageSysStatusAdmin)
