from django.db import models
from django.utils.html import format_html

from apps.users.models import BaseModel, Users


# Create your models here.

class CustomerServer(BaseModel):
    user = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="内容")

    class Meta:
        verbose_name = "客服"
        verbose_name_plural = verbose_name
        db_table = "customer_server"

    def __str__(self):
        return "{}:{}".format(self.user, self.content)

    info_html = "<div>{}</div>"

    def user_username(self):
        return format_html(self.info_html, self.user.username)

    user_username.short_description = "用户名"

    def user_phone(self):
        return format_html(self.info_html, self.user.phone)

    user_phone.short_description = "手机号"

    def user_image(self):
        return format_html('<img src="/media/{}" style="width:64px;height:auto">', self.user.image)

    user_image.short_description = "用户头像"
