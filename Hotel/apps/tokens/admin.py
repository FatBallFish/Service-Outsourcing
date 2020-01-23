from django.contrib import admin
from apps.tokens.models import Tokens


# Register your models here.
class TokensAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Token信息", {'fields': ('token', 'expire_time', 'count', 'enduring')}),
        (
        "用户", {'fields': ('user', 'user_username', 'user_name', 'user_age', 'user_gender', 'user_phone', 'user_image')})
    )
    readonly_fields = ('count', 'user_username', 'user_name', 'user_age', 'user_gender', 'user_phone', 'user_image')
    # 列表页显示内容
    list_display = ('token', 'user', 'expire_time', 'enduring')
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('token', 'user__username', 'enduring')  # 列表搜索字段
    list_filter = ('user__username', 'enduring')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(Tokens, TokensAdmin)
