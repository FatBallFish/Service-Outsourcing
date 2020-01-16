from django.db import models
from apps.users.models import BaseModel, Users

# Create your models here.

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

# 附带功能
def Doki2(token: str) -> tuple:
    Token_list = Tokens.objects.filter(token=token)
    if len(Token_list) != 1:
        return False, ""
    Token = Token_list[0]
    Token.expire_time = datetime.now() + timedelta(minutes=10)
    Token.save()
    if len(Token_list) != 1:
        return False, ""
    Token = Token_list[0]
    Token.expire_time = datetime.now() + timedelta(minutes=10)
    user = Token.user
    Token.save()
    return True, user
