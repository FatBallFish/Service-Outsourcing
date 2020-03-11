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
from apps.guests.models import Orders

from extral_apps.m_arcface import main as Arcface
from extral_apps import MD5

import json, base64


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
                # todo do device api
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
                condition = Q()
                order_list = Orders
                locker_order = LockerOrder.objects.filter(locker__hotel=hotel)
