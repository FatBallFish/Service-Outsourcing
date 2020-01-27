from django.contrib import admin
from django.utils.html import format_html

from apps.faces.models import FaceData, FaceGroup


# Register your models here.
class FaceDataAdmin(admin.ModelAdmin):
    # 编辑界面
    # fields = (('name','sex'),'content','sign','pic','faces_group',)
    fieldsets = (
        ("基本信息", {'fields': ('ID', ('name', 'gender'), 'content')}),
        ("特征信息", {"fields": ("read_sign", "read_img", "if_local"), "classes": ("collaspe", 'wide'),
                  "description": "<strong>人脸信息特征，建议不要手动修改</strong>"}),
        ("人员库信息", {"fields": ("faces_group", "group_id", "group_name", "group_content")})
    )
    radio_fields = {"gender": admin.HORIZONTAL}  # 以单选框形式显示内容，默认为组合框。
    # 参数：垂直布局：admin.VERTICAL  水平布局：admin.HORIZONTAL
    readonly_fields = ("read_sign", "read_img", "if_local", "group_id", "group_name", "group_content")

    def read_sign(self, faces_data):
        """
        :param: faces_data: 传入的是下方被注册的model
        """
        return format_html(
            '<br /><br /><div style="width:100%;height:auto;word-wrap:break-word;word-break:break-all;">{}</div>',
            faces_data.sign)

    read_sign.short_description = "特征值"

    def read_img(self, faces_data):
        if faces_data.if_local == True:
            return format_html('<img src="/media/{}" style="width:100px;height:auto">', faces_data.pic)
        else:
            return format_html('<img src="{}" style="width:100px;height:auto">', faces_data.cos_pic)

    read_img.short_description = "注册图片"
    # 显示界面
    # fields 和 fieldsets不能共存
    list_display = ('img_pic', 'ID', 'name', 'content', 'gender', 'faces_group')  # 列表中显示的字段
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = ('ID', 'img_pic', 'name')  # 列表中可点击跳转的字段
    # list_editable = ('content', 'sex', 'faces_group')  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # list_editable = ('faces_group',)  # 列表中可编辑的字段,注意：可list_display_links与list_editable不可使用相同字段
    # 上面那个有点难看，取消

    search_fields = ('name', 'content')  # 列表搜索字段
    list_filter = ('name', 'content', 'faces_group')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


class FaceGroupAdmin(admin.ModelAdmin):
    fieldsets = (
        ("人员库信息", {'fields': ('id', 'name', 'content')}),
    )
    # 参数：垂直布局：admin.VERTICAL  水平布局：admin.HORIZONTAL
    # readonly_fields = ("group_id",)
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'content')  # 列表中显示的字段
    list_display_links = list_display  # 列表中可点击跳转的字段

    search_fields = list_display  # 列表搜索字段
    list_filter = list_display  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100


admin.site.register(FaceData, FaceDataAdmin)
admin.site.register(FaceGroup, FaceGroupAdmin)
