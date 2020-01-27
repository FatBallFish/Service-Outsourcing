from django.contrib import admin

# Register your models here.
from apps.realauth.models import RealAuth


class RealAuthAdmin(admin.ModelAdmin):
    fieldsets = (
        ("证件信息",
         {'fields': ('id_type', 'ID', 'name', 'gender', 'nation', 'birthday', 'address')}),
        ("签发信息", {'fields': ('organization', 'date_start', 'date_end')}),
        ("额外信息", {'fields': ('add_time', 'update_time')}),
    )
    list_display = ("name", "gender", "nation", 'id_type', 'ID')
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = ('ID', "name", "address")  # 列表搜索字段
    list_filter = ("id_type", "gender", "nation", "birthday")  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(RealAuth, RealAuthAdmin)
