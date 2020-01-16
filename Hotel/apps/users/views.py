from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth import authenticate
from Hotel import settings

from apps.tokens.models import Tokens
from extral_apps import MD5

from datetime import datetime, timedelta
import json, base64
import os, time


# Create your views here.
# COS.Initialize(settings.BASE_DIR)
# Arcface.Initialize(False)

def createToken(username: str, time_int: float) -> str:
    time_now = int(time_int)
    token = MD5.md5(username + str(time_now), "Hotel")
    return token


class UserLoginView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = dict(json.loads(request.body))
            print(data)
        except:
            json_dict = {"id": -1, "status": -1, "message": "Error JSON key", "data": {}}
            return JsonResponse(json_dict)
        if "id" in data.keys():
            id = data["id"]
        else:
            id = -1
        # 判断指定所需字段是否存在，若不存在返回status -1 json。
        for key in ["type", "subtype", "data"]:
            if key not in data.keys():
                # status -1 json的key错误。
                json_dict = {"id": id, "status": -1, "message": "Error JSON key", "data": {}}
                return JsonResponse(json_dict)
        # 处理json
        if data["type"] == "login":
            if data["subtype"] == "pass":
                data = data["data"]
                for key in data.keys():
                    if key not in ["username", "pass", "enduring"]:
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                username = data["username"]
                password = data["pass"]
                if "enduring" in data.keys():
                    enduring = data["enduring"]
                    if not isinstance(enduring, int):
                        enduring = 0
                    if enduring != 0:
                        enduring = 1
                else:
                    # enduring字段未传入，默认为假
                    enduring = 0
                user = authenticate(request, username=username, password=password)
                if user is None:
                    # 未查询到用户
                    json_dict = {"id": id, "status": 100, "message": "Error username or password", "data": {}}
                    return JsonResponse(json_dict)
                # 删除过期及多余的token
                Tokens.objects.filter(expire_time__lt=datetime.now()).delete()
                token_list = Tokens.objects.filter(user=user).order_by("-add_time")[10:]
                for r_token in token_list:
                    Tokens.objects.filter(token=r_token.token).delete()
                # 创建token并返回
                time_now = time.time()
                token = createToken(username, time_now)
                # 创建Tokens实例类
                Token = Tokens()
                Token.user = user
                Token.token = token
                Token.expire_time = datetime.now() + timedelta(minutes=10)
                if enduring == 1:
                    Token.enduring = True
                try:
                    Token.save()
                except Exception as e:
                    print(e)
                    # status 300 token添加失败
                    return JsonResponse({"id": id, "status": 300, "message": "Add Token Failed", "data": {}})
                # status 0 登录成功，获取用户信息
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {"token": token}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
