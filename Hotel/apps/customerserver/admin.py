from django.contrib import admin
from apps.customerserver.models import CustomerServer


# Register your models here.
class CustomerServerAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ('id', 'user', 'content')}),
        ("用户信息", {'fields': ('user_username', 'user_phone', 'user_image')}),
    )
    readonly_fields = ('id', 'user_username', 'user_phone', 'user_image')
    # 列表页显示内容
    list_display = ('id', 'user', 'content')
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('id', 'user__username', 'content')  # 列表搜索字段
    list_filter = ('id', 'user__username', 'content')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(CustomerServer, CustomerServerAdmin)
