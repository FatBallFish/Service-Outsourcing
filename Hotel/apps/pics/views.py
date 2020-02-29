from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from Hotel import settings

from apps.pics.models import PicBed
from extral_apps import MD5
from extral_apps.m_cos import py_cos_main as COS
import json, os, base64


# Create your views here.

class PicView(View):
    def get(self, request, *args, **kwargs):
        try:
            name = str(request.GET.get("name"))
            print("value:", name)
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        if name is None or name == "":
            return HttpResponseRedirect("/media/default/error.jpg")
        # 处理upload的特殊模式
        upload_to = os.path.join(kwargs["upload_to"])
        if upload_to == "users":
            try:
                picbed = PicBed.objects.get(upload_to=upload_to, name=name)
            except Exception as e:
                return HttpResponseRedirect("/media/users/default.jpg")
        elif upload_to == "faces_data":
            return HttpResponseRedirect("/media/default/error.jpg")
        else:
            try:
                picbed = PicBed.objects.get(upload_to=upload_to, name=name)
            except Exception as e:
                return HttpResponseRedirect("/media/default/error.jpg")
        if_local = picbed.if_local
        if if_local:
            return HttpResponseRedirect(picbed.local_url.url)
        else:
            return HttpResponseRedirect(picbed.cos_url.url)

    def post(self, request, *args, **kwargs):
        # try:
        #     token = request.GET.get("token")
        #     print("token:", token)
        # except Exception as e:
        #     print(e)
        #     print("Missing necessary args")
        #     # log_main.error("Missing necessary agrs")
        #     # status -100 缺少必要的参数
        #     return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        # result, user = Doki2(token=token)
        # if result is False:
        #     return JsonResponse({"id": -1, "status": -101, "message": "Error Token", "data": {}})
        try:
            data = dict(json.loads(request.body))
            # print(data)
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
        if type == "pic":
            if subtype == "upload":
                for key in ["name", "base64", "upload_to"]:
                    if key not in data.keys():
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                # name / type 处理
                img_name = str(data["name"])
                img_type = "pic"
                if "type" in data.keys():
                    img_type = str(data["type"])

                # upload_to特殊处理
                upload_to = os.path.join(str(data["upload_to"]).replace("/", "\\"))
                if upload_to in ["faces_data", "faces_data\\"]:
                    # status 200 权限不足
                    return JsonResponse({"id": id, "status": 200, "message": "No right to operate", "data": {}})
                if upload_to == "users":
                    img_type = "user"
                # ------------------------------------------------

                if_local = False
                if "if_local" in data.keys():
                    if_local = data["if_local"]
                    if not isinstance(if_local, bool):
                        if_local = False
                content = ""
                if "content" in data.keys():
                    content = data["content"]
                # 处理 base64
                img_base64 = str(data["base64"])
                base64_head_index = img_base64.find(";base64,")
                if base64_head_index != -1:
                    print("进行了替换")
                    img_base64 = img_base64.partition(";base64,")[2]
                try:
                    img_file = base64.b64decode(img_base64)
                except Exception as e:
                    # status 100 错误的图片数据
                    return JsonResponse({"id": id, "status": 100, "message": "Error Base64 data", "data": {}})

                # 更换md5加密方式
                md5 = MD5.md5(upload_to + img_name)
                pic_name = md5 + "." + img_type
                file_name = os.path.join(upload_to, pic_name)
                # 将upload_to转换回去
                upload_to = upload_to.replace("\\", "/")
                if if_local:
                    result, url = LocalWrite(file_name, img_file)
                else:
                    result, url = CosWrite(file_name, img_file)
                local_url = None
                cos_url = None
                if result:
                    if if_local:
                        local_url = url
                        url = "/media/" + url
                    else:
                        cos_url = url
                else:
                    if if_local:
                        # status -600 本地上传失败
                        return JsonResponse({"id": id, "status": -600, "message": "Local upload Error", "data": {}})
                    else:
                        # status -500 本地上传失败
                        return JsonResponse({"id": id, "status": -500, "message": "COS upload Error", "data": {}})
                defaults = {"content": content, "md5": md5, "if_local": if_local, "local_url": local_url,
                            "cos_url": cos_url}
                PicBed.objects.update_or_create(defaults=defaults, name=img_name, upload_to=upload_to)
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {"url": url}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


def PicUrl(file_name: str) -> str:
    path = file_name.split("\\")
    path = "/".join(path)
    # path = path
    return path


def LocalWrite(file_name: str, bytes: bytes) -> tuple:
    path_list = file_name.split("\\")
    file = path_list.pop(-1)
    path = "\\".join(path_list)
    path = os.path.join(settings.MEDIA_ROOT, path)
    os.makedirs(path, exist_ok=True)
    path = os.path.join(path, file)
    try:
        with open(path, "wb") as f:
            f.write(bytes)
        url = PicUrl(file_name)
    except Exception as e:
        return False, ""
    return True, url


def CosWrite(file_name: str, bytes: bytes) -> tuple:
    path = file_name.split("\\")
    path = "/".join(path)
    print(path)
    try:
        COS.bytes_upload(body=bytes, key=path)
    except Exception as e:
        print(e)
        return False, ""
    path = settings.COS_ROOTURL + path
    return True, path
