from django.shortcuts import render
from Hotel import settings

from django.views import View
from django.http.response import JsonResponse

from apps.devices.models import Device, DeviceDoki, GetBindDevice
from apps.rooms.models import Hotel

from extral_apps import MD5

import json


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
                if "device_name" not in data.keys():
                    # status -3 json的value错误。
                    return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                device_name = str(data["device_name"])
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
                                               device_content=device_content, hotel=hotel)
                return JsonResponse(
                    {"id": id, "status": 0, "message": "Successful", "data": {"device_id": device.device_id}})
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
