from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse
from django.db.models import Q

from apps.tokens.models import Doki2
from apps.users.models import Users
from apps.guests.models import Orders
from apps.rooms.models import Hotel
from apps.locker.models import Locker, LockerOrder
from apps.msg.models import Messages, MessageText

from datetime import datetime, timedelta
import json
import random
import time


# Create your views here.
class LockerApplyView(View):
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
        if type == "locker":
            if subtype == "apply":
                for key in ["order_id"]:
                    if key not in data.keys():
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                order_id = data["order_id"]
                try:
                    order = Orders.objects.get(id=order_id)
                except Exception as e:
                    # status 100 错误的订单id
                    return JsonResponse({"id": id, "status": 100, "message": "Error order_id", "data": {}})
                if user != order.guest.user:
                    # status 300 用户与订单的预订人不一致
                    return JsonResponse({"id": id, "status": 300, "message": "User mismatch", "data": {}})
                if not user.face:
                    # status 301 用户无人脸数据
                    return JsonResponse({"id": id, "status": 301, "message": "User don't has face data", "data": {}})
                if order.status not in [1, 2]:  # 如果不是预约中和入住中两种状态
                    # status 101 错误的订单状态
                    return JsonResponse({"id": id, "status": 101, "message": "Error order status", "data": {}})
                start_time = order.date_start
                end_time = order.date_end
                now = datetime.now()
                if not ((now > start_time - timedelta(hours=6)) and (now < start_time + timedelta(hours=3))):
                    # status 102 错误的预约时间
                    return JsonResponse({"id": id, "status": 102, "message": "Error apply time", "data": {}})
                locker_order_list = LockerOrder.objects.filter(
                    Q(user=user) & (~Q(status="canceled") & ~Q(status="done")))
                if len(locker_order_list) > 0:
                    # status 103 已有未完成的预约或使用记录
                    return JsonResponse({"id": id, "status": 103, "message": "Already had application", "data": {}})
                hotel = order.hotel
                locker_list = Locker.objects.filter(hotel=hotel).filter(available=True).filter(used=False)
                if len(locker_list) == 0:
                    # status 200 该酒店无可用寄存柜
                    return JsonResponse({"id": id, "status": 200, "message": "No available locker", "data": {}})
                locker = random.choice(locker_list)
                defaults = {"status": "applying", "expire_time": start_time + timedelta(hours=3),
                            "add_time": datetime.now(), "update_time": datetime.now()}
                locker_order, result = LockerOrder.objects.update_or_create(defaults=defaults, user=user, locker=locker,
                                                                            order=order)
                locker.used = True
                locker.save()
                msg_result = self.sendApplyMessage(user=user, locker_order=locker_order)
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"apply_id": locker_order.id, "status": locker_order.status,
                                              "locker_id": locker.id, "index": locker.index, "num": locker.num,
                                              "expire_time": locker_order.expire_time.timestamp()}})
            elif subtype == "cancel":
                if "apply_id" not in data.keys():
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                apply_id = data["apply_id"]
                try:
                    locker_order = LockerOrder.objects.get(id=apply_id)
                except Exception as e:
                    # status 100 错误的预约信息id
                    return JsonResponse({"id": id, "status": 100, "message": "Error apply_id", "data": {}})
                if locker_order.user != user:
                    # status 300 用户与预约者不一致
                    return JsonResponse({"id": id, "status": 300, "message": "User mismatch", "data": {}})
                if locker_order.status != "applying":
                    # status 101 只有预约状态下可取消预约
                    return JsonResponse(
                        {"id": id, "status": 101, "message": "Only with applying status can be canceled", "data": {}})
                locker = locker_order.locker
                locker_order.status = "canceled"
                locker_order.save()
                locker.used = False
                locker.save()
                msg_result = self.sendCancelMessage(user=user, locker_order=locker_order)
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})

    def sendApplyMessage(self, user: Users, locker_order: LockerOrder) -> bool:
        locker = locker_order.locker
        try:
            hotel = Users.objects.get(username="hotel")
        except Exception as e:
            hotel = None
        title = "预约寄存柜成功"
        content = "您成功预约了{}的寄存柜，以下是详细信息,请注意过期时间，过时自动取消".format(locker.hotel.name)
        extra = {"hotel_id": locker.hotel.id, "hotel_name": locker.hotel.name, "apply_id": locker_order.id,
                 "status": locker_order.status, "locker_id": locker.id, "index": locker.index, "num": locker.num,
                 "expire_time": locker_order.expire_time.timestamp()}
        msg_text, result = MessageText.objects.update_or_create(title=title, content=content)
        data_dict = {
            "type": "locker",
            "subtype": "apply",
            "sendID": hotel,
            "recID": user,
            "text": msg_text,
            "extra": json.dumps(extra),
            "status": None,
        }
        msg = Messages.objects.create(**data_dict)
        if not msg:
            return False
        return True

    def sendCancelMessage(self, user: Users, locker_order: LockerOrder) -> bool:
        locker = locker_order.locker
        try:
            hotel = Users.objects.get(username="hotel")
        except Exception as e:
            hotel = None
        title = "取消寄存柜成功"
        content = "您已成功取消预约{}的寄存柜，以下是详细信息".format(locker.hotel.name)
        extra = {"hotel_id": locker.hotel.id, "hotel_name": locker.hotel.name, "apply_id": locker_order.id,
                 "status": locker_order.status, "locker_id": locker.id, "index": locker.index, "num": locker.num,
                 "expire_time": locker_order.expire_time.timestamp()}
        msg_text, result = MessageText.objects.update_or_create(title=title, content=content)
        data_dict = {
            "type": "locker",
            "subtype": "cancel",
            "sendID": hotel,
            "recID": user,
            "text": msg_text,
            "extra": json.dumps(extra),
            "status": None,
        }
        msg = Messages.objects.create(**data_dict)
        if not msg:
            return False
        return True


class LockerInfoView(View):
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
        if type == "locker":
            if subtype == "list":
                if "order_id" not in data.keys():
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                order_id = data["order_id"]
                locker_order_status = None
                if "status" in data.keys():
                    locker_order_status = data["status"]
                    if locker_order_status not in ["applying", "using", "canceled", "done"]:
                        locker_order_status = None
                try:
                    order = Orders.objects.get(id=order_id)
                except Exception as e:
                    # status 100 错误的订单id
                    return JsonResponse({"id": id, "status": 100, "message": "Error order_id", "data": {}})
                if user != order.guest.user:
                    # status 300 用户与订单的预订人不一致
                    return JsonResponse({"id": id, "status": 300, "message": "User mismatch", "data": {}})
                if locker_order_status:
                    condition = Q(order=order) & Q(user=user) & Q(status=locker_order_status)
                else:
                    condition = Q(order=order) & Q(user=user)
                lo_list = LockerOrder.objects.filter(condition).order_by("-add_time")
                data_list = []
                for locker_order in lo_list:
                    locker = locker_order.locker
                    data_dict = {"apply_id": locker_order.id, "status": locker_order.status, "locker_id": locker.id,
                                 "index": locker.index, "num": locker.num,
                                 "expire_time": locker_order.expire_time.timestamp()}
                    data_list.append(data_dict)
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"num": len(data_list), "list": data_list}})
            elif subtype == "get":
                if "apply_id" not in data.keys():
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                apply_id = data["apply_id"]
                try:
                    locker_order = LockerOrder.objects.get(id=apply_id)
                except Exception as e:
                    # status 100 错误的寄存柜预约信息id
                    return JsonResponse({"id": id, "status": 100, "message": "Error apply id", "data": {}})
                if user != locker_order.user:
                    # status 300 用户与预约者不一致
                    return JsonResponse({"id": id, "status": 300, "message": "User mismatch", "data": {}})
                locker = locker_order.locker
                data_dict = {"apply_id": locker_order.id, "status": locker_order.status, "locker_id": locker.id,
                             "index": locker.index, "num": locker.num,
                             "expire_time": locker_order.expire_time.timestamp()}
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": data_dict})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})