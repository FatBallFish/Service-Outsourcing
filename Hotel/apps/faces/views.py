from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from Hotel import settings

from apps.tokens.models import Doki2
from apps.faces.models import FaceGroup, FaceData
from extral_apps import MD5
from extral_apps.m_arcface import main as Arcface

import json, base64
import os


# Create your views here.

# COS.Initialize(settings.BASE_DIR)
# Arcface.Initialize(False)

class FaceGroupView(View):
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
        if type == "group":  ## 用户信息api
            if subtype == "create":
                # 用户权限检查
                if not user.is_staff:
                    # status -103 无权操作
                    return JsonResponse({"id": id, "status": -103, "message": "No Permission Operate", "data": {}})
                for key in ["group_name", "group_content"]:
                    if key not in data.keys():
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                group_name = data["name"]
                group_content = data["content"]
                try:
                    FaceGroup.objects.get(name=group_name)
                    # status 100 人员库名称已存在
                    return JsonResponse({"id": id, "status": 100, "message": "FaceGroup name has existed", "data": {}})
                except Exception as e:
                    try:
                        face_group = FaceGroup()
                        face_group.name = group_name
                        face_group.content = group_content
                        face_group.save()
                        # status 0 成功
                        return JsonResponse(
                            {"id": id, "status": 0, "message": "Successful", "data": {"group_id": face_group.id}})
                    except Exception as e:
                        print(e)
                        # status 101 创建人员库失败
                        return JsonResponse({"id": id, "status": 101, "message": "Create FaceGroup Failed", "data": {}})
            elif subtype == "update":
                # 用户权限检查
                if not user.is_staff:
                    # status -103 无权操作
                    return JsonResponse({"id": id, "status": -103, "message": "No Permission Operate", "data": {}})
                group_id: int = None
                group_name: str = None
                group_content: str = None
                for key in data.keys():
                    if key not in ["group_id", "group_name", "group_content"]:
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                    if key == "group_id":
                        group_id = data[key]
                        if isinstance(group_id, str):
                            if group_id.isdecimal():
                                group_id = int(group_id)
                            else:
                                # status 100 错误的人员库ID
                                return JsonResponse({"id": id, "status": 100, "message": "Error Group ID", "data": {}})
                        elif not isinstance(group_id, int):
                            # status 100 错误的人员库ID
                            return JsonResponse({"id": id, "status": 100, "message": "Error Group ID", "data": {}})
                    elif key == "group_name":
                        group_name = str(data[key])
                    elif key == "group_content":
                        group_content = str(data[key])
                if group_id is None and group_name is None:
                    # status 101 需要人员库ID或者人员库名称
                    return JsonResponse({"id": id, "status": 101, "message": "Need Group ID or Group name", "data": {}})
                else:
                    if group_id is not None:
                        try:
                            face_group = FaceGroup.objects.get(id=group_id)
                        except Exception as e:
                            # status 102 无此人员库
                            return JsonResponse({"id": id, "status": 102, "message": "No such Group", "data": {}})
                    else:
                        try:
                            face_group = FaceGroup.objects.get(name=group_name)
                        except Exception as e:
                            # status 102 无此人员库
                            return JsonResponse({"id": id, "status": 102, "message": "No such Group", "data": {}})
                    face_group.content = group_content
                    face_group.save()
                    # status 0 成功
                    return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {}})
            elif subtype == "delete":
                # 用户权限检查
                if not user.is_staff:
                    # status -103 无权操作
                    return JsonResponse({"id": id, "status": -103, "message": "No Permission Operate", "data": {}})
                group_id: int = None
                group_name: str = None
                for key in data.keys():
                    if key not in ["group_id", "group_name"]:
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                    if key == "group_id":
                        group_id = data[key]
                        if isinstance(group_id, str):
                            if group_id.isdecimal():
                                group_id = int(group_id)
                            else:
                                # status 100 错误的人员库ID
                                return JsonResponse({"id": id, "status": 100, "message": "Error Group ID", "data": {}})
                        elif not isinstance(group_id, int):
                            # status 100 错误的人员库ID
                            return JsonResponse({"id": id, "status": 100, "message": "Error Group ID", "data": {}})
                    elif key == "group_name":
                        group_name = str(data[key])
                if group_id is None and group_name is None:
                    # status 101 需要人员库ID或者人员库名称
                    return JsonResponse({"id": id, "status": 101, "message": "Need Group ID or Group name", "data": {}})
                else:
                    if group_id is not None:
                        try:
                            face_group = FaceGroup.objects.get(id=group_id)
                        except Exception as e:
                            # status 102 无此人员库
                            return JsonResponse({"id": id, "status": 102, "message": "No such Group", "data": {}})
                    else:
                        try:
                            face_group = FaceGroup.objects.get(name=group_name)
                        except Exception as e:
                            # status 102 无此人员库
                            return JsonResponse({"id": id, "status": 102, "message": "No such Group", "data": {}})
                    try:
                        face_group.delete()
                    except Exception as e:
                        # status 103 删除人员库失败
                        return JsonResponse({"id": id, "status": 103, "message": "Delete Group Failed", "data": {}})
                    # status 0 成功
                    return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {}})
            elif subtype == "get":
                group_id: int = None
                group_name: str = None
                group_content: str = None
                for key in data.keys():
                    if key not in ["group_id", "group_name"]:
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                    if key == "group_id":
                        group_id = data[key]
                        if isinstance(group_id, str):
                            if group_id.isdecimal():
                                group_id = int(group_id)
                            else:
                                # status 100 错误的人员库ID
                                return JsonResponse({"id": id, "status": 100, "message": "Error Group ID", "data": {}})
                        elif not isinstance(group_id, int):
                            # status 100 错误的人员库ID
                            return JsonResponse({"id": id, "status": 100, "message": "Error Group ID", "data": {}})
                    elif key == "group_name":
                        group_name = str(data[key])
                    elif key == "group_content":
                        group_content = str(data[key])
                if group_id is None and group_name is None:
                    # status 101 需要人员库ID或者人员库名称
                    return JsonResponse({"id": id, "status": 101, "message": "Need Group ID or Group name", "data": {}})
                else:
                    if group_id is not None:
                        try:
                            face_group = FaceGroup.objects.get(id=group_id)
                        except Exception as e:
                            # status 102 无此人员库
                            return JsonResponse({"id": id, "status": 102, "message": "No such Group", "data": {}})
                    else:
                        try:
                            face_group = FaceGroup.objects.get(name=group_name)
                        except Exception as e:
                            # status 102 无此人员库
                            return JsonResponse({"id": id, "status": 102, "message": "No such Group", "data": {}})
                    # status 0 成功
                    return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                         "data": {"group_id": face_group.id, "group_name": face_group.name,
                                                  "group_content": face_group.content}})
            elif subtype == "list":
                face_group_list = FaceGroup.objects.all()
                data_list = []
                for face_group in face_group_list:
                    data_dict = {"group_id": face_group.id, "group_name": face_group.name,
                                 "group_content": face_group.content}
                    data_list.append(data_dict)
                # status 0 成功
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"num": len(data_list), "list": data_list}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class FaceView(View):
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
        type = data["type"]
        subtype = data["subtype"]
        data = data["data"]
        if type == "face":
            if subtype == "register":
                for key in ["name", "base64", "faces_group_id"]:
                    if key not in data.keys():
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                face_name = data["name"]
                img_base64 = data["base64"]

                # 获取人员库id并检查
                faces_group_id = data["faces_group_id"]
                try:
                    faces_group = FaceGroup.objects.get(group_id=faces_group_id)
                except Exception as e:
                    return JsonResponse({"id": id, "status": 100, "message": "Faces group not exist", "data": {}})

                base64_head_index = img_base64.find(";base64,")
                if base64_head_index != -1:
                    print("进行了替换")
                    img_base64 = img_base64.partition(";base64,")[2]
                # print("-------接收到数据-------\n", img_base64, "\n-------数据结构尾-------")
                img_type = "face"
                # if "type" in data.keys():
                #     img_type = data["type"]
                img_file = base64.b64decode(img_base64)
                pic_name = MD5.md5(face_name) + "." + img_type
                file_name = os.path.join(settings.BASE_DIR, "media", "faces_data", pic_name)
                with open(file_name, "wb") as f:
                    f.write(img_file)
                # 信息初始写入 姓名，特征，注册图片
                Arcface.addFace(path=file_name, name=face_name)
                # 获取性别，人员库等其他信息
                face_dict = Arcface.checkFace(file_name)
                sex = face_dict["gender"]
                face_content = ""
                if "content" in data.keys():
                    face_content = data["content"]
                try:
                    face_data = FaceData.objects.get(name=face_name)
                except Exception as e:
                    print(e)
                    return JsonResponse({"id": id, "status": 101, "message": "Register face failed", "data": {}})
                face_data.faces_group = faces_group
                face_data.sex = sex
                face_data.content = face_content
                face_data.save()
                json_dict = {"id": id, "status": 0, "message": "successful", "data": {}}
                return JsonResponse(json_dict)
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        elif type == "check":
            if subtype == "facedata":
                for key in data.keys():
                    if key not in ["base64", "type"]:
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                img_base64 = data["base64"]
                base64_head_index = img_base64.find(";base64,")
                if base64_head_index != -1:
                    print("进行了替换")
                    img_base64 = img_base64.partition(";base64,")[2]
                # print("-------接收到数据-------\n", img_base64, "\n-------数据结构尾-------")
                img_type = "face"
                # if "type" in data.keys():
                #     img_type = data["type"]
                img_file = base64.b64decode(img_base64)
                pic_name = MD5.md5_bytes(img_file) + "." + img_type
                file_name = os.path.join(settings.BASE_DIR, "media", "tmp", pic_name)
                with open(file_name, "wb") as f:
                    f.write(img_file)
                json_dict = Arcface.checkFace(file_name)
                # json_dict = {"id": id, "status": 0, "message": "successful", "data": {}}
                return JsonResponse(json_dict)
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})

        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})

    def get(self, request, *args, **kwargs):
        pass
