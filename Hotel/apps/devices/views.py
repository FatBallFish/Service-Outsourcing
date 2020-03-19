from django.shortcuts import render
from Hotel import settings

from django.views import View
from django.http.response import JsonResponse
from django.db.models import Q

from apps.faces.models import FaceGroup, FaceData
from apps.devices.models import Device, DeviceDoki, DeviceGroup
from apps.rooms.models import Hotel, HotelFaceGroup
from apps.users.models import Users
from apps.locker.models import LockerOrder, Locker
from apps.guests.models import Orders, GuestRoom
from apps.msg.models import MessageText, Messages
from apps.passengerFlow.models import PassengerFlow, PassengerFace

from extral_apps.m_arcface import main as Arcface
from extral_apps import MD5

from datetime import datetime, timedelta
from typing import Tuple
import json, base64, random, time


# Create your views here.
class DeviceLoginView(View):
    def post(self, request, *args, **kwargs):
        try:
            device_id = request.GET.get("device_id")
            print("device_id:", device_id)
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        result, device = DeviceDoki(device_id=device_id)
        if result is False:
            return JsonResponse({"id": -1, "status": -101, "message": "Error Token", "data": {}})
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
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
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "device":
            if subtype == "login":
                if "password" not in data.keys():
                    # status -3 json的value错误。
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                password = data["password"]
                password = MD5.md5(password, "hotel")
                if device.password != password:
                    # status 100 Error Password
                    return JsonResponse({"id": id, "status": 100, "message": "Error Password", "data": {}})
                # status 0 successful
                json_dict = {"id": id, "status": 0, "message": "Successful",
                             "data": {"host": settings.HP_SOCKET_IP, "port": settings.HP_SOCKET_PORT,
                                      "flag": settings.HP_SOCKET_FLAG, "maxsize": settings.HP_SOCKET_MAXSIZE,
                                      "device_id": device_id}}
                return JsonResponse(json_dict)
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class DeviceRegisterView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
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
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "device":
            if subtype == "register":
                for key in ["device_name", "password"]:
                    if key not in data.keys():
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                device_name = str(data["device_name"])
                password = str(data["password"])
                password = MD5.md5(password, "hotel")
                device_content = None
                if "device_content" in data.keys():
                    device_content = str(data["device_content"])
                device_id = MD5.md5(device_name)
                hotel_id = None
                hotel = None
                if "hotel_id" in data.keys():
                    hotel_id = data["hotel_id"]
                    if isinstance(hotel_id, str):
                        if hotel_id.isdecimal():
                            hotel_id = int(hotel_id)
                    elif isinstance(hotel_id, int):
                        pass
                    else:
                        # status 100 错误的酒店id
                        return JsonResponse({"id": id, "status": 100, "message": "Error Hotel id", "data": {}})
                    try:
                        hotel = Hotel.objects.get(id=hotel_id)
                    except Exception as e:
                        # status 100 错误的酒店id
                        return JsonResponse({"id": id, "status": 100, "message": "Error Hotel id", "data": {}})
                try:
                    Device.objects.get(device_name=device_name)
                    # status 101 设备名已存在
                    return JsonResponse({"id": id, "status": 101, "message": "device_name already exist", "data": {}})
                except Exception as e:
                    pass
                device = Device.objects.create(device_id=device_id, device_name=device_name,
                                               device_content=device_content, hotel=hotel, password=password)
                return JsonResponse(
                    {"id": id, "status": 0, "message": "Successful", "data": {"device_id": device.device_id}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class DeviceListView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
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
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "device":
            if subtype == "list":
                if "hotel_id" not in data.keys():
                    # status -3 json的value错误。
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                try:
                    hotel_id = int(data["hotel_id"])
                except Exception as e:
                    # status -203 键值对的数据类型错误
                    return JsonResponse({"id": id, "status": -203, "message": "Arg's value type error", "data": {}})
                device_list = Device.objects.filter(hotel_id=hotel_id)
                data_list = []
                for device in device_list:
                    device_dict = {"device_id": device.device_id, "device_name": device.device_name,
                                   "device_content": device.device_content, "is_online": device.is_online}
                    data_list.append(device_dict)
                # status 0 成功处理事件
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"num": len(data_list), "list": data_list}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class DeviceHotelListView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
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
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "hotel":
            if subtype == "list":
                hotel_list = Hotel.objects.all()
                data_list = []
                for hotel in hotel_list:
                    data_dict = {"id": hotel.id, "name": hotel.name, "content": hotel.content,
                                 "address": hotel.location}
                    data_list.append(data_dict)
                json_dict = {"id": id, "status": 0, "message": "Successful",
                             "data": {"num": len(data_list), "list": data_list}}
                return JsonResponse(json_dict)
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class DeviceFaceFeatureView(View):
    def post(self, request, *args, **kwargs):
        try:
            device_id = request.GET.get("device_id")
            print("device_id:", device_id)
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        result, device = DeviceDoki(device_id=device_id)
        if result is False:
            return JsonResponse({"id": -1, "status": -104, "message": "Error device_id token", "data": {}})
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
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
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "feature":
            if subtype == "list":
                if "db" in data.keys():
                    db = str(data["db"])
                    try:
                        db = int(db)
                    except ValueError:
                        db = 1
                else:
                    db = 1
                if db == -1:
                    face_list = FaceData.objects.all()
                else:
                    face_list = FaceData.objects.filter(faces_group_id=db)
                data_list = []
                for face in face_list:
                    face_dict = {"ID": face.ID, "name": face.name, "gender": face.gender, "content": face.content,
                                 "sign": face.sign, "pic_url": face.pic.url if face.if_local else face.cos_pic.url,
                                 "db": db}
                    data_list.append(face_dict)
                # status 0 处理成功
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"num": len(data_list), "list": data_list}})
            elif subtype == "get":
                if "ID" in data.keys():
                    ID = str(data["ID"])
                else:
                    # status -3 json的value错误。
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                try:
                    face = FaceData.objects.get(ID=ID)
                except Exception as e:
                    # status 100 错误的ID
                    return JsonResponse({"id": id, "status": 100, "message": "Error ID", "data": {}})
                face_dict = {"ID": face.ID, "name": face.name, "gender": face.gender, "content": face.content,
                             "sign": face.sign, "pic_url": face.pic.url if face.if_local else face.cos_pic.url,
                             "db": face.faces_group.id}
                # status 0 成功处理
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": face_dict})
            elif subtype == "hotel":
                if "hotel_id" not in data.keys():
                    # status -3 json的value错误。
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                try:
                    hotel_id = int(data["hotel_id"])
                except Exception as e:
                    # status -203 键值对的数据类型错误
                    return JsonResponse({"id": id, "status": -203, "message": "Arg's value type error", "data": {}})
                hotel_face_group_list = HotelFaceGroup.objects.filter(hotel_id=hotel_id)
                num = len(hotel_face_group_list)
                condition = None
                if num != 0:
                    condition = Q(faces_group_id=hotel_face_group_list[0].face_group.id)
                    for hotel_face_group in hotel_face_group_list:
                        condition = condition | Q(faces_group_id=hotel_face_group.face_group.id)
                    face_list = FaceData.objects.filter(condition)
                else:
                    face_list = []  # 直接为空列表
                data_list = []
                for face in face_list:
                    face_dict = {"ID": face.ID, "name": face.name, "gender": face.gender, "content": face.content,
                                 "sign": face.sign, "pic_url": face.pic.url if face.if_local else face.cos_pic.url,
                                 "db": face.faces_group.id}
                    data_list.append(face_dict)
                # status 0 处理成功
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"num": len(data_list), "list": data_list}})
            elif subtype == "device":
                device_group_list = DeviceGroup.objects.filter(device=device)
                num = len(device_group_list)
                condition = None
                if num != 0:
                    condition = Q(faces_group_id=device_group_list[0].faces_group.id)
                    for device_group in device_group_list:
                        condition = condition | Q(faces_group_id=device_group.faces_group.id)
                    face_list = FaceData.objects.filter(condition)
                else:
                    face_list = []  # 直接为空列表
                data_list = []
                for face in face_list:
                    face_dict = {"ID": face.ID, "name": face.name, "gender": face.gender, "content": face.content,
                                 "sign": face.sign, "pic_url": face.pic.url if face.if_local else face.cos_pic.url,
                                 "db": face.faces_group.id}
                    data_list.append(face_dict)
                # status 0 处理成功
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"num": len(data_list), "list": data_list}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class DeviceLockerView(View):
    def post(self, request, *args, **kwargs):
        try:
            device_id = request.GET.get("device_id")
            print("device_id:", device_id)
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        result, device = DeviceDoki(device_id=device_id)
        if result is False:
            return JsonResponse({"id": -1, "status": -104, "message": "Error device_id token", "data": {}})
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
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
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "locker":
            if subtype == "verify":
                if "feature" not in data.keys():
                    # status -3 json的value错误。
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                feature_b64 = data["feature"]
                feature = base64.b64decode(feature_b64)
                ID, threshold = Arcface.face_compare(feature=feature)
                if threshold == 0:
                    # status 100 未匹配相关人脸
                    return JsonResponse({"id": id, "status": 100, "message": "Not matching face data", "data": {}})
                try:
                    face = FaceData.objects.get(ID=ID)
                except Exception as e:
                    # status 101 错误的face_id
                    return JsonResponse({"id": id, "status": 101, "message": "Error face id", "data": {}})
                try:
                    user = Users.objects.get(face=face)
                except Exception as e:
                    # status 102 该人脸未绑定用户账号
                    return JsonResponse({"id": id, "status": 102, "message": "The face data not bind user", "data": {}})
                hotel = device.hotel
                locker_order_list = LockerOrder.objects.filter(
                    Q(locker__hotel=hotel) & Q(status="applying") & Q(user=user))
                if len(locker_order_list) == 0:
                    # status 200 无预定信息
                    return JsonResponse({"id": id, "status": 200, "message": "No applying records", "data": {}})
                elif len(locker_order_list) > 1:
                    # status 201 订单记录异常
                    return JsonResponse({"id": id, "status": 201, "message": "applying records abnormal", "data": {}})
                locker_order = locker_order_list[0]
                locker_order.status = "using"
                locker_order.expire_time = datetime.now()
                locker_order.save()
                self.sendUsedMessage(user=user, locker_order=locker_order)
                data_dict = {"locker_id": locker_order.locker.id, "locker_index": locker_order.locker.index,
                             "locker_num": locker_order.locker.num, "expire_time": locker_order.expire_time.timestamp(),
                             "user_id": locker_order.user.username,
                             "name": locker_order.user.real_auth.name, "gender": locker_order.user.real_auth.gender}
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": data_dict})
            elif subtype == "order_list":
                if "ID" not in data.keys():
                    # status -3 json的value错误。
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                ID = str(data["ID"])
                try:
                    faceData = FaceData.objects.get(ID=ID)
                except Exception as e:
                    # status 101 错误的face_id
                    return JsonResponse({"id": id, "status": 101, "message": "Error face id", "data": {}})
                try:
                    user = Users.objects.get(face=faceData)
                except Exception as e:
                    # status 102 该人脸未绑定用户账号
                    return JsonResponse({"id": id, "status": 102, "message": "The face data not bind user", "data": {}})
                hotel = device.hotel
                order_list = Orders.objects.filter(
                    Q(hotel=hotel) & Q(guest__user=user) & (Q(status=1) | Q(status=2))).order_by("-add_time")
                data_list = []
                for order in order_list:
                    data_dict = {"order_id": order.id, "date_start": order.date_start.timestamp(),
                                 "date_end": order.date_end.timestamp(),
                                 "room": "{}({})".format(order.room.number, order.room.name)}
                    data_list.append(data_dict)
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"num": len(data_list), "list": data_list}})
            elif subtype == "apply":
                for key in ["order_id"]:
                    if key not in data.keys():
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                order_id = data["order_id"]
                try:
                    order = Orders.objects.get(id=order_id)
                except Exception as e:
                    # status 100 错误的订单id
                    return JsonResponse({"id": id, "status": 100, "message": "Error order_id", "data": {}})
                user = order.guest.user
                if not user.face:
                    # status 301 用户无人脸数据
                    return JsonResponse({"id": id, "status": 301, "message": "User don't has face data", "data": {}})
                if order.status not in [1, 2]:  # 如果不是预约中和入住中两种状态
                    # status 101 错误的订单状态
                    return JsonResponse({"id": id, "status": 101, "message": "Error order status", "data": {}})

                locker_order_list = LockerOrder.objects.filter(
                    Q(user=user) & (~Q(status="canceled") & ~Q(status="done")))
                if len(locker_order_list) > 0:
                    # status 103 已有未完成的预约或使用记录
                    return JsonResponse({"id": id, "status": 103, "message": "Already had application", "data": {}})

                start_time = order.date_start
                end_time = order.date_end
                now = datetime.now()
                if not ((now > start_time - timedelta(hours=6)) and (now < start_time + timedelta(hours=3))):
                    # status 102 错误的预约时间
                    return JsonResponse({"id": id, "status": 102, "message": "Error apply time", "data": {}})

                hotel = order.hotel
                if hotel != device.hotel:
                    # status 104 订单酒店与设备酒店不一致
                    return JsonResponse({"id": id, "status": 104, "message": "Error hotel", "data": {}})
                locker_list = Locker.objects.filter(hotel=hotel).filter(available=True).filter(used=False)
                if len(locker_list) == 0:
                    # status 200 该酒店无可用寄存柜
                    return JsonResponse({"id": id, "status": 200, "message": "No available locker", "data": {}})
                locker = random.choice(locker_list)
                defaults = {"status": "using", "expire_time": end_time + timedelta(hours=1),
                            "add_time": datetime.now(), "update_time": datetime.now()}
                locker_order, result = LockerOrder.objects.update_or_create(defaults=defaults, user=user, locker=locker,
                                                                            order=order)
                locker.used = True
                locker.save()
                GuestRoom.objects.filter(order=order).update(if_locker=1)
                msg_result = self.sendUsedMessage(user=user, locker_order=locker_order)
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"apply_id": locker_order.id, "status": locker_order.status,
                                              "locker_id": locker.id, "index": locker.index, "num": locker.num,
                                              "expire_time": locker_order.expire_time.timestamp(),
                                              "user_id": user.username, "name": user.real_auth.name,
                                              "gender": user.real_auth.gender}})
            elif subtype == "get":
                if "feature" not in data.keys():
                    # status -3 json的value错误。
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                feature_b64 = data["feature"]
                feature = base64.b64decode(feature_b64)
                ID, threshold = Arcface.face_compare(feature=feature)
                if threshold == 0:
                    # status 100 未匹配相关人脸
                    return JsonResponse({"id": id, "status": 100, "message": "Not matching face data", "data": {}})
                try:
                    face = FaceData.objects.get(ID=ID)
                except Exception as e:
                    # status 101 错误的face_id
                    return JsonResponse({"id": id, "status": 101, "message": "Error face id", "data": {}})
                try:
                    user = Users.objects.get(face=face)
                except Exception as e:
                    # status 102 该人脸未绑定用户账号
                    return JsonResponse({"id": id, "status": 102, "message": "The face data not bind user", "data": {}})
                hotel = device.hotel
                locker_order_list = LockerOrder.objects.filter(
                    Q(locker__hotel=hotel) & Q(status="using") & Q(user=user))
                if len(locker_order_list) == 0:
                    # status 200 无预定信息
                    return JsonResponse({"id": id, "status": 200, "message": "No using records", "data": {}})
                elif len(locker_order_list) > 1:
                    # status 201 订单记录异常
                    return JsonResponse({"id": id, "status": 201, "message": "applying records abnormal", "data": {}})
                locker_order = locker_order_list[0]
                locker_order.status = "done"
                locker_order.save()
                locker = locker_order.locker
                locker.used = False
                locker.save()
                self.sendDoneMessage(user=user, locker_order=locker_order)
                data_dict = {"locker_id": locker.id, "locker_index": locker.index,
                             "locker_num": locker.num, "expire_time": locker_order.expire_time.timestamp(),
                             "user_id": locker_order.user.username,
                             "name": locker_order.user.real_auth.name, "gender": locker_order.user.real_auth.gender}
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": data_dict})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})

    def sendUsedMessage(self, user: Users, locker_order: LockerOrder) -> bool:
        locker = locker_order.locker
        try:
            hotel = Users.objects.get(username="hotel")
        except Exception as e:
            hotel = None
        title = "寄存柜已打开，请及时存放物品"
        content = "您已成功打开了寄存柜，请及时存储物品，退房前请不要忘记取回哦。寄存柜将为您保管物品至您退房一小时后，逾期请联系前台取回"
        extra = {"hotel_id": locker.hotel.id, "hotel_name": locker.hotel.name, "apply_id": locker_order.id,
                 "status": locker_order.status, "locker_id": locker.id, "index": locker.index, "num": locker.num,
                 "expire_time": locker_order.expire_time.timestamp()}
        msg_text, result = MessageText.objects.update_or_create(title=title, content=content)
        data_dict = {
            "type": "locker",
            "subtype": "using",
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

    def sendDoneMessage(self, user: Users, locker_order: LockerOrder) -> bool:
        locker = locker_order.locker
        try:
            hotel = Users.objects.get(username="hotel")
        except Exception as e:
            hotel = None
        title = "感谢您使用寄存柜"
        content = "您申请了取出寄存物，请及时取出物品，检查有无遗漏，并在取出物品后将寄存柜关好，谢谢您的配合。"
        extra = {"hotel_id": locker.hotel.id, "hotel_name": locker.hotel.name, "apply_id": locker_order.id,
                 "status": locker_order.status, "locker_id": locker.id, "index": locker.index, "num": locker.num,
                 "expire_time": locker_order.expire_time.timestamp()}
        msg_text, result = MessageText.objects.update_or_create(title=title, content=content)
        data_dict = {
            "type": "locker",
            "subtype": "done",
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


class DevicePassengerFlowView(View):
    def post(self, request, *args, **kwargs):
        try:
            device_id = request.GET.get("device_id")
            print("device_id:", device_id)
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        result, device = DeviceDoki(device_id=device_id)
        if result is False:
            return JsonResponse({"id": -1, "status": -104, "message": "Error device_id token", "data": {}})
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
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
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "passenger":
            if subtype == "flow":
                for key in ["hotel_id", "sign", "age", "gender", "location"]:
                    if key not in data.keys():
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                try:
                    hotel_id: int = int(data["hotel_id"])
                except Exception as e:
                    # status -203 键值对数据类型错误
                    return JsonResponse({"id": id, "status": -203, "message": "Arg's value type error", "data": {}})
                try:
                    hotel = Hotel.objects.get(id=hotel_id)
                except Exception as e:
                    # status 100 错误的酒店id
                    return JsonResponse({"id": id, "status": 100, "message": "Error hotel id", "data": {}})
                try:
                    age: int = int(data["age"])
                except Exception as e:
                    age = -1
                gender = str(data["gender"])
                if gender not in ["male", "female"]:
                    gender: str = "unknown"
                location: str = str(data["location"])
                sign: str = str(data["sign"])
                ID: str = None
                name: str = "stranger"
                mask: bool = None
                enter_time: datetime = datetime.now()
                exit_time: datetime = None
                if "mask" in data.keys():
                    mask = bool(data["mask"])
                if "enter_time" in data.keys():
                    enter_time_stamp = float(data["enter_time"])
                    enter_time = datetime.fromtimestamp(enter_time_stamp)
                if "exit_time" in data.keys():
                    exit_time_stamp = float(data["exit_time"])
                    exit_time = datetime.fromtimestamp(exit_time_stamp)
                # 查找人脸是否在实名认证库中，没有进行下一步的客流数据库查找
                check_face_group_result, check_face_group_ID, check_face_group_dict = self.checkFaceFromGroup(sign=sign)

                # 查找人脸记录是否在客流数据库中，没有自动创建
                check_face_flow_result, check_face_flow_ID = self.checkFaceFromFlow(sign=sign)

                if check_face_flow_result:
                    # 人脸在客流数据库中存在
                    try:
                        passenger_face = PassengerFace.objects.get(ID=check_face_flow_ID)
                    except Exception as e:
                        # status 200 错误的客流人脸id
                        return JsonResponse({"id": 0, "status": 200, "message": "Error Passenger face ID", "data": {}})
                    if check_face_group_result:
                        # 数据库中有记录且客流库中也有记录，判断数据是否一致，不一致将把客流库中的数据修改成人员库的数据
                        ID = check_face_group_dict["ID"]
                        name = check_face_group_dict["name"]
                        gender = check_face_group_dict["gender"]
                        if passenger_face.ID != ID:
                            passenger_face.ID = ID
                        if passenger_face.name != name:
                            passenger_face.name = name
                        if passenger_face.gender != gender:
                            passenger_face.gender = gender
                        passenger_face.save()
                else:
                    # 人脸在客流数据库中不存在
                    if check_face_group_result:
                        # 客流不存在但人员库中有记录存在，说明是老客，将老客数据直接加入到客流数据库中
                        ID = check_face_group_dict["ID"]
                        name = check_face_group_dict["name"]
                        gender = check_face_group_dict["gender"]
                        passenger_face = PassengerFace.objects.create(ID=ID, name=name, age=age, gender=gender,
                                                                      sign=sign, mask=mask)
                    else:
                        # 纯新客，所有数据新创建
                        if ID is None:
                            ID = str(int(time.time() * 1000))
                        passenger_face = PassengerFace.objects.create(ID=ID, name=name, age=age, gender=gender,
                                                                      sign=sign, mask=mask)
                # 检查此客流信息是否在10min之内出现过，若出现过自动跳过不记录
                check_flow_result = self.checkFaceAppearTime(ID=ID, enter_time=enter_time, location=location)
                if check_flow_result is None:
                    # 出错
                    return JsonResponse({"id": id, "status": 2, "message": "Error", "data": {}})
                elif check_flow_result is True:
                    # 出现过
                    return JsonResponse({"id": id, "status": 1, "message": "Had appeared in 10 minutes", "data": {}})
                else:
                    # 未出现过
                    passenger_face.num += 1
                    passenger_face.save()
                    record_dict = {
                        "face": passenger_face,
                        "enter_time": enter_time,
                        "exit_time": exit_time,
                        "hotel": hotel,
                        "location": location
                    }
                    PassengerFlow.objects.create(**record_dict)
                    return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {}})

    def checkFaceFromGroup(self, sign: str) -> Tuple[bool, str, dict]:
        """
        检查人脸是否在人员数据库中

        :param sign: 人脸特征
        :return:
        """
        try:
            sign_bytes = base64.b64decode(sign)
        except Exception as e:
            return False, "", {}
        opt_ID, max_threshold = Arcface.face_compare(sign_bytes)
        data_dict = {}
        if max_threshold != 0.0:
            try:
                face = FaceData.objects.get(ID=opt_ID)
            except Exception as e:
                return False, "", {}
            data_dict["ID"] = opt_ID
            data_dict["name"] = face.name
            data_dict["gender"] = face.gender
            data_dict["threshold"] = max_threshold
            return True, opt_ID, data_dict
        else:
            return False, "", {}

    def checkFaceFromFlow(self, sign: str) -> Tuple[bool, str]:
        """
        检测人脸是否在客流数据库中

        :param sign: 人脸特征
        :return:
        """
        try:
            sign_bytes = base64.b64decode(sign)
        except Exception as e:
            raise e
            return False, ""
        pass_list = PassengerFlow.objects.all()
        # Arcface.load_passenger_features()
        for passenger in pass_list:
            face = passenger.face
            if not face.sign:
                continue
            sign2 = face.sign
            try:
                sign_bytes2 = base64.b64decode(sign2)
            except Exception as e:
                raise e
                return False, ""
            threshold = Arcface.face_compare_only(sign_bytes, sign_bytes2)
            if threshold != 0.0:
                return True, face.ID
        return False, ""

    def checkFaceAppearTime(self, ID: str, enter_time: datetime, location: str) -> bool:
        """
        检测人脸10min内是否出现过

        :param ID: 人脸ID
        :return: 出现过返回True，未出现过返回False，失败返回None
        """
        try:
            passenger_face = PassengerFace.objects.get(ID=ID)
        except Exception as e:
            return None
        check_time1 = enter_time
        check_time2 = check_time1 - timedelta(minutes=10)
        pass_list = PassengerFlow.objects.filter(
            Q(face=passenger_face) & Q(enter_time__lte=check_time1) & Q(enter_time__gte=check_time2) & Q(
                location=location))
        # Arcface.load_passenger_features()
        if len(pass_list) != 0:
            return True
        return False
