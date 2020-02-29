from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from Hotel import settings

from apps.tokens.models import Doki2
from apps.faces.models import FaceGroup, FaceData
from apps.realauth.models import RealAuth
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
        data = dict(data["data"])
        if type == "face":
            if subtype == "register":
                if user.real_auth is None:
                    # todo 以此为模版更改人证核验的api返回值
                    # todo 增加人员库不存在的情况返回
                    print("未实名认证")
                    return JsonResponse({"id": id, "status": 100, "message": "RealAuth not certified", "data": {}})
                for key in ["base64", "db"]:
                    if key not in data.keys():
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                face_name = user.real_auth.name
                face_ID = user.real_auth.ID
                img_base64 = data["base64"]
                db = 1  # 默认人脸库
                # 获取人员库id并检查
                if "db" in data.keys():
                    db = data["db"]
                try:
                    faces_group = FaceGroup.objects.get(id=db)
                except Exception as e:
                    # status 100 人员库不存在
                    return JsonResponse({"id": id, "status": 100, "message": "Faces group not exist", "data": {}})
                base64_head_index = img_base64.find(";base64,")
                if base64_head_index != -1:
                    print("进行了替换")
                    img_base64 = img_base64.partition(";base64,")[2]
                img_type = "face"
                img_file = base64.b64decode(img_base64)
                # todo 更改存储方式，由name转为ID
                pic_name = MD5.md5(face_ID) + "." + img_type
                file_name = os.path.join(settings.BASE_DIR, "media", "faces_data", pic_name)
                with open(file_name, "wb") as f:
                    f.write(img_file)
                # 先检查人脸数，如果不等于1，返回错误状态码
                face_dict = Arcface.checkFace(file_name)
                num = face_dict["num"]
                if num == 0:
                    # 注册的图片无人脸
                    # status 102 图片中无人脸数据
                    return JsonResponse({"id": id, "status": 102, "message": "No face data in base64", "data": {}})
                    # todo 完善无脸或两张脸以上的情况！
                elif num > 1:
                    # status 103 图片中人脸数据过多
                    return JsonResponse(
                        {"id": id, "status": 103, "message": "Too much face data in base64", "data": {}})
                # 信息初始写入 姓名，特征，注册图片
                Arcface.addFace(path=file_name, name=face_name, ID=face_ID)
                # 获取性别，人员库等其他信息
                face_dict = Arcface.checkFace(file_name)
                num = face_dict["num"]
                data_list = face_dict["list"]
                if num == 1:
                    face_dict = data_list[0]
                elif num == 0:
                    # 注册的图片无人脸
                    # status 102 图片中无人脸数据
                    return JsonResponse({"id": id, "status": 102, "message": "No face data in base64", "data": {}})
                    # todo 完善无脸或两张脸以上的情况！
                else:
                    # status 103 图片中人脸数据过多
                    return JsonResponse(
                        {"id": id, "status": 103, "message": "Too much face data in base64", "data": {}})
                gender = face_dict["gender"]
                face_content = ""
                if "content" in data.keys():
                    face_content = data["content"]
                try:
                    face_data = FaceData.objects.get(ID=face_ID)
                except Exception as e:
                    print(e)
                    # status 101 注册人脸数据失败
                    return JsonResponse({"id": id, "status": 101, "message": "Register face failed", "data": {}})
                face_data.faces_group = faces_group
                face_data.gender = gender
                face_data.content = face_content
                face_data.save()
                user.face = face_data
                user.save()
                json_dict = {"id": id, "status": 0, "message": "successful", "data": {"face_id": face_data.ID}}
                return JsonResponse(json_dict)
            elif subtype == "find":
                for key in ["base64", "db"]:
                    if key not in data.keys():
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                try:
                    db = int(data["db"])
                except Exception as e:
                    db = -1
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
                # todo 优化本地存储性能
                with open(file_name, "wb") as f:
                    f.write(img_file)
                # Arcface.reload_features(db=db)
                json_dict = Arcface.checkFace(file_name, db=db)
                print(json_dict)
                num = json_dict["num"]
                data_list = json_dict["list"]
                if num == 0:  # 无人脸数据
                    # if not json_dict:  # 无人脸数据
                    # status 100 图片中无人脸数据
                    return JsonResponse({"id": id, "status": 100, "message": "No face data in base64", "data": {}})
                ret_type = 0
                if "ret_type" in data.keys():
                    if isinstance(data["ret_type"], str):
                        if str(data["ret_type"]).isdecimal():
                            ret_type = int(data["ret_type"])
                    elif isinstance(data["ret_type"], int):
                        ret_type = data["ret_type"]
                    else:
                        ret_type = 0
                sample_list = []
                for face_dict in data_list:
                    ID = face_dict["ID"]
                    try:
                        face_data = FaceData.objects.get(ID=ID)
                        name = face_data.name
                        face_dict["name"] = name
                    except Exception as e:
                        name = ""
                        face_dict["name"] = name
                    liveness = face_dict["liveness"]
                    threshold = face_dict["threshold"]
                    sample_dict = {"ID": ID, "name": name, "liveness": liveness, "threshold": threshold}
                    sample_list.append(sample_dict)
                if ret_type == 0:  # 简略返回，result，liveness，threshold
                    return JsonResponse({"id": id, "status": 0, "message": "successful",
                                         "data": {"num": len(sample_list), "list": sample_list}})
                else:
                    # status 0 successful
                    return JsonResponse({"id": id, "status": 0, "message": "successful", "data": json_dict})
            elif subtype == "verify":
                print(user.face)
                if not user.face:
                    # status 100 人脸未认证 No authentication
                    return JsonResponse({"id": id, "status": 100, "message": "No face authentication", "data": {}})
                for key in ["base64"]:
                    if key not in data.keys():
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
                # todo 优化本地存储性能
                with open(file_name, "wb") as f:
                    f.write(img_file)
                # Arcface.reload_features(db=db)
                json_dict = Arcface.checkFace(file_name, user=user)
                num = json_dict["num"]
                data_list = json_dict["list"]
                if num == 0:
                    # if not json_dict:
                    # status 101 图片中无人脸数据
                    return JsonResponse({"id": id, "status": 101, "message": "No face data in base64", "data": {}})
                elif num != 1:
                    # status 102 图片中人脸数据过多
                    return JsonResponse(
                        {"id": id, "status": 102, "message": "Too much face data in base64", "data": {}})
                ret_type = 0
                if "ret_type" in data.keys():
                    if isinstance(data["ret_type"], str):
                        if str(data["ret_type"]).isdecimal():
                            ret_type = int(data["ret_type"])
                    elif isinstance(data["ret_type"], int):
                        ret_type = data["ret_type"]
                    else:
                        ret_type = 0
                # todo 数据格式转换（两处）
                # todo 去除加载数据库时的打印，以及请求到达时的base64打印
                # todo 完成两个认证api以及绑定api
                # todo 2020年1月27日00:20:34
                # {'num': 1, 'list': [
                #     {'ID': '331082199911270890', 'age': 21, 'threshold': 1.0, 'gender': 'female', 'liveness': True,
                #      'top_left': (399, 413), 'top_right': (658, 413), 'bottom_left': (399, 672),
                #      'bottom_right': (658, 672)}]}
                face_dict = data_list[0]
                ID = face_dict["ID"]
                liveness = face_dict["liveness"]
                threshold = face_dict["threshold"]
                check_result = True if ID == user.face.ID else False
                sample_dict = {"result": check_result, "ID": ID, "liveness": liveness, "threshold": threshold}
                if ret_type == 0:  # 简略返回，result，liveness，threshold
                    return JsonResponse({"id": id, "status": 0, "message": "successful",
                                         "data": sample_dict})
                else:
                    face_dict["result"] = check_result
                    # status 0 successful
                    return JsonResponse({"id": id, "status": 0, "message": "successful", "data": face_dict})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        elif type == "feature":
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
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


def get(self, request, *args, **kwargs):
    pass
