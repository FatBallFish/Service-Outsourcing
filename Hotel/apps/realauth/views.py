from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from Hotel import settings

from apps.tokens.models import Doki2
from apps.realauth.models import RealAuth

from datetime import datetime
import time
import json


# Create your views here.
class RealAuthView(View):
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
        ## -------正式处理事务-------
        data = dict(data["data"])
        if type == "realauth":  ## 用户信息api
            if subtype == "create":
                real_info = {
                    'id_type': "sfz",
                    'id': "",
                    'name': "",
                    'gender': "",
                    'nation': None,
                    'birthday': None,
                    'address': None,
                    'organization': None,
                    'date_start': None,
                    'date_end': None
                }
                for key in ['id_type', 'id', 'name', 'gender', 'birthday']:
                    if key not in data.keys():
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                    elif key == "id_type":
                        if data[key] == "sfz":
                            real_info[key] = data[key]
                        else:
                            # status 200 Error id_type
                            return JsonResponse({"id": id, "status": 200, "message": "Error id_type", "data": {}})
                    elif key == "id":
                        real_info[key] = str(data[key])
                    elif key == "name":
                        real_info[key] = str(data[key])
                    elif key == "gender":
                        if data[key] not in ["male", "female"]:
                            # status 201 Error gender
                            return JsonResponse({"id": id, "status": 201, "message": "Error gender", "data": {}})
                        real_info[key] = data[key]
                    elif key == "birthday":
                        try:
                            timestamp = float(data[key])
                        except Exception as e:
                            # status 202
                            return JsonResponse({"id": id, "status": 202, "message": "Error birthday", "data": {}})
                        time_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                        real_info[key] = datetime.strptime(time_str, "%Y-%m-%d").date()
                if "nation" in data.keys():
                    real_info["nation"] = str(data["nation"])
                if "address" in data.keys():
                    real_info["address"] = str(data["address"])
                if "organization" in data.keys():
                    real_info["organization"] = str(data["organization"])
                if "date_start" in data.keys():
                    try:
                        timestamp = float(data["date_start"])
                    except Exception as e:
                        # status 203 错误的开始日期
                        return JsonResponse({"id": id, "status": 203, "message": "Error date_start", "data": {}})
                    time_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                    real_info["date_start"] = datetime.strptime(time_str, "%Y-%m-%d").date()
                if "date_end" in data.keys():
                    try:
                        timestamp = float(data["date_end"])
                    except Exception as e:
                        # status 204 错误的结束日期
                        return JsonResponse({"id": id, "status": 204, "message": "Error date_end", "data": {}})
                    time_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                    real_info["date_end"] = datetime.strptime(time_str, "%Y-%m-%d").date()
                try:
                    real_auth = RealAuth()
                    real_auth.id_type = real_info["id_type"]
                    real_auth.ID = real_info["id"]
                    real_auth.name = real_info["name"]
                    real_auth.gender = real_info["gender"]
                    real_auth.nation = real_info["nation"]
                    real_auth.birthday = real_info["birthday"]
                    real_auth.address = real_info["address"]
                    real_auth.organization = real_info["organization"]
                    real_auth.date_start = real_info["date_start"]
                    real_auth.date_end = real_info["date_end"]
                    real_auth.save()
                    user.real_auth = real_auth
                    user.save()
                except Exception as e:
                    # status 100 创建实名认证失败
                    return JsonResponse({"id": id, "status": 100, "message": "Create RealAuth failed", "data": {}})
                # status 0 成功处理事件
                return JsonResponse(
                    {"id": id, "status": 0, "message": "Successful", "data": {"real_auth_id": real_auth.ID}})
            elif subtype == "update":
                real_auth = user.real_auth
                if not real_auth:
                    # status 100 实名未认证
                    return JsonResponse({"id": id, "status": 100, "message": "RealAuth not certified", "data": {}})
                real_info = {
                    'nation': user.real_auth.nation,
                    'address': user.real_auth.address,
                    'organization': user.real_auth.organization,
                    'date_start': user.real_auth.date_start,
                    'date_end': user.real_auth.date_end
                }
                for key in data.keys():
                    if key not in ['nation', 'address', 'organization', 'date_start', "date_end"]:
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                    elif key in ["date_start", "date_end"]:
                        try:
                            timestamp = float(data[key])
                        except Exception as e:
                            # status 200 错误的date信息
                            return JsonResponse(
                                {"id": id, "status": 200, "message": "Error {}".format(key), "data": {}})
                        time_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                        real_info[key] = datetime.strptime(time_str, "%Y-%m-%d").date()
                    else:
                        real_info[key] = str(data[key])
                real_auth.nation = real_info["nation"]
                real_auth.address = real_info["address"]
                real_auth.organization = real_info["organization"]
                real_auth.date_start = real_info["date_start"]
                real_auth.date_end = real_info["date_end"]
                real_auth.save()
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {}})
            elif subtype == "get":
                real_auth = user.real_auth
                if not real_auth:
                    # status 100 实名未认证
                    return JsonResponse({"id": id, "status": 100, "message": "RealAuth not certified", "data": {}})
                data_dict = {
                    "id_type": real_auth.id_type,
                    "id": real_auth.ID,
                    "name": real_auth.name,
                    "gender": real_auth.gender,
                    "nation": real_auth.nation,
                    "birthday": time.mktime(real_auth.birthday.timetuple()),
                    "address": real_auth.address,
                    "organization": real_auth.organization,
                    "date_start": time.mktime(real_auth.date_start.timetuple()),
                    "date_end": time.mktime(real_auth.date_end.timetuple())
                }
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": data_dict})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
