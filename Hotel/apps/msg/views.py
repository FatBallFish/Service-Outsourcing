from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse

from apps.tokens.models import Users, Doki2
from apps.msg.models import Messages, MessageSysStatus, MessageText
from apps.msg.models import getNewSysMessageNum, getSysMessage, getNewPrivateNum, getPrivateMessage

import json


# Create your views here.
class MsgView(View):
    def post(self, request, *args, **kwargs):
        try:
            token = request.GET.get("token")
            print("token:", token)
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        result, user = Doki2(token=token)
        print("result:{},user:{}".format(result, user))
        if result is False:
            return JsonResponse({"id": -1, "status": -101, "message": "Error Token", "data": {}})
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
            print(e)
            # status -1 json的key错误。此处id是因为没有进行读取，所以返回默认的-1。
            return JsonResponse({"id": -1, "status": -1, "message": "Error JSON key", "data": {}})
            # 先获取json里id的值，若不存在，默认值为-1
        if "id" in data.keys():
            id = data["id"]
        else:
            id = -1
        ## 判断指定所需字段是否存在，若不存在返回status -1 json。
        for key in ["type", "subtype", "data"]:
            if key not in data.keys():
                # status -1 json的key错误。
                return JsonResponse({"id": id, "status": -1, "message": "Error JSON key", "data": {}})
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "msg":
            if subtype == "has_new":
                private_dict = getNewPrivateNum(user=user)
                num_private = private_dict["total"]
                num_sys = getNewSysMessageNum(user=user)
                num = num_private + num_sys
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"sys": num_sys, "private": num_private,
                                              "private_detail": private_dict["detail"]}})
            elif subtype == "sys":
                if_new = 0  # 0为新消息，1为旧消息，2为新消息，错误代码默认为新消息
                if "if_new" in data.keys():
                    try:
                        if_new = int(data["if_new"])
                    except Exception as e:
                        if_new = 0
                if if_new not in [0, 1, 2]:
                    if_new = 0
                json_dict = getSysMessage(user=user, if_new=if_new, id=id)
                print(json_dict)
                return JsonResponse(json_dict)
            elif subtype == "private":
                if_new = 0  # 0为新消息，1为旧消息，2为新消息，错误代码默认为新消息
                if "if_new" in data.keys():
                    try:
                        if_new = int(data["if_new"])
                    except Exception as e:
                        if_new = 0
                if if_new not in [0, 1, 2]:
                    if_new = 0
                json_dict = getPrivateMessage(user=user, if_new=if_new, id=id)
                return JsonResponse(json_dict)
            elif subtype == "send":
                for key in ["receiver", "title", "content"]:
                    if key not in data.keys():
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                receiver = str(data["receiver"])
                title = str(data["title"])
                content = str(data["content"])
                try:
                    recID = Users.objects.get(username=receiver)
                except Exception as e:
                    # status 100 错误的接收者
                    return JsonResponse({"id": id, "status": 100, "message": "Error receiver", "data": {}})
                try:
                    msgtext, result = MessageText.objects.get_or_create(title=title, content=content)
                    # if not result:
                    #     # status 101 创建消息内容失败
                    #     return JsonResponse(
                    #         {"id": id, "status": 101, "message": "Create MessageText Failed", "data": {}})
                except Exception as e:
                    # status 101 创建消息内容失败
                    return JsonResponse({"id": id, "status": 101, "message": "Create MessageText Failed", "data": {}})
                msg = Messages()
                msg.sendID = user
                msg.recID = recID
                msg.text = msgtext
                msg.status = False
                msg.save()
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {"msg_id": msg.id}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
