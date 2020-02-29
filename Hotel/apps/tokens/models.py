from django.db import models
from django.utils.html import format_html

from apps.users.models import BaseModel, Users

# Create your models here.
from typing import Tuple
from datetime import datetime, timedelta


class Tokens(BaseModel):
    token = models.CharField(verbose_name="许可证", primary_key=True, max_length=64)
    user = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.CASCADE)
    expire_time = models.DateTimeField(verbose_name="过期时间")
    count = models.IntegerField(verbose_name="token计数", default=1)
    enduring = models.BooleanField(verbose_name="是否长效登录", default=False)

    class Meta:
        verbose_name = "tokens"
        verbose_name_plural = verbose_name
        db_table = "tokens"

    def __str__(self):
        return "{user}:{token}".format(user=self.user.username, token=self.token)

    info_html = "<div>{}</div>"

    def user_username(self):
        return format_html(self.info_html, self.user.username)

    user_username.short_description = "用户名"

    def user_name(self):
        return format_html(self.info_html, self.user.last_name + self.user.first_name)

    user_name.short_description = "姓名"

    def user_phone(self):
        return format_html(self.info_html, self.user.phone)

    user_phone.short_description = "手机号"

    def user_image(self):
        return format_html('<img src="/api/pic/get/users?name={}" style="width:64px;height:auto">', self.user.username)

    user_image.short_description = "用户头像"


# 附带功能
def Doki2(token: str) -> Tuple[bool, Users]:
    Token_list = Tokens.objects.filter(token=token)
    if len(Token_list) != 1:
        return False, None
    Token = Token_list[0]
    Token.expire_time = datetime.now() + timedelta(minutes=10)
    Token.save()
    user = Token.user
    return True, user
