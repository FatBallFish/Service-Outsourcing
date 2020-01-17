from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from Hotel import settings

from apps.faces.models import FaceGroup, FaceData
from extral_apps import MD5
from extral_apps.m_arcface import main as Arcface

import json, base64
import os

# Create your views here.

# COS.Initialize(settings.BASE_DIR)
# Arcface.Initialize(False)


class FaceRegisterView(View):
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
        type = data["type"]
        subtype = data["subtype"]
        data = data["data"]
        if type == "register":
            if subtype == "facedata":
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
