from django.contrib import admin
from django.utils.html import format_html

from apps.pics.models import PicBed


# Register your models here.


class PicBedAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("图片信息", {'fields': ('name', 'content', 'md5', 'upload_to', 'if_local', 'local_url', 'cos_url')}),
        ("图片预览", {'fields': ('read_img',)}),
    )
    # radio_fields = {"if_local": admin.HORIZONTAL}  # 以单选框形式显示内容，默认为组合框。

    # 参数：垂直布局：admin.VERTICAL  水平布局：admin.HORIZONTAL
    readonly_fields = ("read_img",)

    def read_img(self, picbed):
        if picbed.if_local is True:
            return format_html('<img src="/media/{}" style="width:100px;height:auto">', picbed.local_url)
        else:
            return format_html('<img src="{}" style="width:100px;height:auto">', picbed.cos_url)

    read_img.short_description = "图片"
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = (
    'id', 'img_pic', 'name', 'content', 'md5', 'upload_to', 'if_local', 'local_url', 'cos_url')  # 列表中显示的字段
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = ('id', 'img_pic', 'name')  # 列表中可点击跳转的字段
    # 上面那个有点难看，取消

    search_fields = ('name', 'local_url', 'cos_url')  # 列表搜索字段
    list_filter = ('name', 'if_local')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(PicBed, PicBedAdmin)
