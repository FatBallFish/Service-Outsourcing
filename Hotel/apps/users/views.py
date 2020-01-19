from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from Hotel import settings

from apps.users.models import Users
from apps.tokens.models import Tokens, Doki2
from extral_apps import MD5
from extral_apps.m_redis import py_redis as Redis
from extral_apps.m_img import py_captcha_main as ImgCaptcha
from extral_apps.m_sms import py_sms_main as SmsCaptcha
from extral_apps.m_cos import py_cos_main as COS
from extral_apps.m_arcface import main as Arcface

from datetime import datetime, timedelta
import json, base64, random
import os, time

# Create your views here.
COS.Initialize(settings.BASE_DIR)
Redis.Initialize(settings.BASE_DIR)
ImgCaptcha.Initialize(settings.BASE_DIR)
SmsCaptcha.Initialize(settings.BASE_DIR)
Arcface.Initialize(False)


def createToken(username: str, time_int: float) -> str:
    time_now = int(time_int)
    token = MD5.md5(username + str(time_now), "Hotel")
    return token


class UserLoginView(View):
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
        # 处理json
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "login":
            if subtype == "pass":
                for key in data.keys():
                    if key not in ["username", "pass", "enduring"]:
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                username = data["username"]
                password = data["pass"]
                if "enduring" in data.keys():
                    enduring = data["enduring"]
                    if not isinstance(enduring, int):
                        enduring = 0
                    if enduring != 0:
                        enduring = 1
                else:
                    # enduring字段未传入，默认为假
                    enduring = 0
                user = authenticate(request, username=username, password=password)
                if user is None:
                    # 未查询到用户
                    json_dict = {"id": id, "status": 100, "message": "Error username or password", "data": {}}
                    return JsonResponse(json_dict)
                # 删除过期及多余的token
                Tokens.objects.filter(expire_time__lt=datetime.now()).delete()
                token_list = Tokens.objects.filter(user=user).order_by("-add_time")[10:]
                for r_token in token_list:
                    Tokens.objects.filter(token=r_token.token).delete()
                # 创建token并返回
                time_now = time.time()
                token = createToken(username, time_now)
                # 创建Tokens实例类
                Token = Tokens()
                Token.user = user
                Token.token = token
                Token.expire_time = datetime.now() + timedelta(minutes=10)
                if enduring == 1:
                    Token.enduring = True
                try:
                    Token.save()
                except Exception as e:
                    print(e)
                    # status 300 token添加失败
                    return JsonResponse({"id": id, "status": 300, "message": "Add Token Failed", "data": {}})
                # status 0 登录成功，获取用户信息
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {"token": token}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class UserRegisterView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
            # status -1 json的key错误。此处id是因为没有进行读取，所以返回默认的-1。
            return JsonResponse({"id": -1, "status": -1, "message": "Error JSON key", "data": {}})
        # 先获取json里id的值，若不存在，默认值为-1
        if "id" in data.keys():
            id = data["id"]
        else:
            id = -1

        # 判断指定所需字段是否存在，若不存在返回status -1 json。
        for key in ["type", "subtype", "data"]:
            if not key in data.keys():
                # status -1 json的key错误。
                return JsonResponse({"id": id, "status": -1, "message": "Error JSON key", "data": {}})
        # 处理json
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "register":
            if subtype == "phone":
                for key in data.keys():
                    if key not in ["username", "hash", "pass"]:
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                username = data["username"]
                hash = data["hash"]
                password = data["pass"]
                # password = MD5.md5(password, "guochuang")
                result = Redis.SafeCheck(hash)
                if not result:
                    # status -4 hash不存在
                    return JsonResponse({"id": id, "status": -4, "message": "Error hash", "data": {}})
                # 创建用户
                try:
                    Users.objects.create_user(username=username, password=password, phone=username)
                except Exception as e:
                    print(e)
                    return JsonResponse({"id": id, "status": 100, "message": "Create User Failed", "data": {}})
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class CaptchaView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = dict(json.loads(request.body))
            print(data)
        except Exception as e:
            # status -1 json的key错误。此处id是因为没有进行读取，所以返回默认的-1。
            return JsonResponse({"id": -1, "status": -1, "message": "Error JSON key", "data": {}})
            # 先获取json里id的值，若不存在，默认值为-1
        if "id" in data.keys():
            id = data["id"]
        else:
            id = -1

        # 判断指定所需字段是否存在，若不存在返回status -1 json。
        for key in ["type", "subtype", "data"]:
            if not key in data.keys():
                # status -1 json的key错误。
                return JsonResponse({"id": id, "status": -1, "message": "Error JSON key", "data": {}})
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        # 处理json
        if type == "img":
            if subtype == "generate":
                # code,addr = ImgCaptcha.CreatCode()
                code, b64_data = ImgCaptcha.CreatCode()
                code = code.lower()  # 将所有的验证码转成小写
                rand_str = ""
                for i in range(5):
                    char1 = random.choice(
                        [chr(random.randint(65, 90)), chr(random.randint(48, 57)), chr(random.randint(97, 122))])
                    rand_str += char1
                hash = MD5.md5(code, salt=rand_str)
                result = Redis.AddImgHash(hash)
                # todo 优化验证机制
                if result == False:
                    # status -404 Unkown Error
                    return JsonResponse({
                        "id": id,
                        "status": -404,
                        "message": "Unknown Error",
                        "data": {}
                    })
                # status 0 ImgCaptcha生成成功
                # return JsonResponse({
                #     "id":id,
                #     "status":0,
                #     "message":"Successful",
                #     "data":{"code":code,"addr":addr,"rand":rand_str}
                return JsonResponse(
                    {"id": id, "status": 0, "message": "Successful", "data": {"imgdata": b64_data, "rand": rand_str}})
            elif subtype == "validate":
                for key in data.keys():
                    if key not in ["hash"]:
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                hash = data["hash"]
                result = Redis.SafeCheck(hash)
                if result == True:
                    # status 0 校验成功。
                    return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {}})
                elif result == False:
                    # status 100 验证码hash值不匹配(包括验证码过期)。
                    return JsonResponse({"id": id, "status": 100, "message": "Error captcha hash", "data": {}})
                else:
                    # status -404 Unkown Error
                    return JsonResponse({"id": id, "status": -404, "message": "Unknown Error", "data": {}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        elif type == "sms":
            if data["subtype"] == "generate":
                for key in ["phone"]:
                    # if key not in ["phone","hash"]:
                    if key not in data.keys():
                        # status -3 Error data key | data_json key错误
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                # hash = data["hash"]
                # result = Redis.SafeCheck(hash)
                # if result != 0:
                #     # status -4 json的value错误。
                #     return JsonResponse({"id": id, "status": -4, "message": "Error Hash", "data": {}})
                phone = str(data["phone"])
                command_type = 1
                if "command_type" in data.keys():
                    command_type = data["command_type"]
                code = random.randint(10000, 99999)
                if command_type == 1:
                    # 注册账号
                    result = SmsCaptcha.SendCaptchaCode(phone_number=phone, captcha=code, command_str="注册账号",
                                                        ext=str(id))
                    print(result)
                elif command_type == 2:
                    # 找回密码
                    result = SmsCaptcha.SendCaptchaCode(phone_number=phone, captcha=code, command_str="找回密码",
                                                        ext=str(id))
                    print(result)
                else:
                    # status -204 Arg's value error 键值对数据错误。
                    return JsonResponse({"id": id, "status": -204, "message": "Arg's value error", "data": {}})
                status = ""
                message = ""
                try:
                    status = result.get("result")
                    message = result.get("errmsg")
                except Exception as e:
                    print(e)
                if message == "OK":
                    message = "Successful"
                rand_str = ""
                if status == 0:
                    for i in range(5):
                        char1 = random.choice(
                            [chr(random.randint(65, 90)), chr(random.randint(48, 57)),
                             chr(random.randint(97, 122))])
                        rand_str += char1
                    hash = MD5.md5(code, salt=rand_str)
                    result = Redis.AddSmsHash(hash)
                    if result == False:
                        # status -404 Unkown Error
                        return JsonResponse({"id": id, "status": -404, "message": "Unknown Error", "data": {}})
                    # status 0 SmsCaptcha生成成功
                    return JsonResponse({"id": id, "status": status, "message": message, "data": {"rand": rand_str}})
                    # 改动：将code字段删除
                else:
                    # status=result["result"] 遇到错误原样返回腾讯云信息
                    return JsonResponse({"id": id, "status": status, "message": message, "data": {}})
            elif data["subtype"] == "validate":
                for key in data.keys():
                    if key not in ["hash"]:
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                hash = data["hash"]
                result = Redis.SafeCheck(hash)
                if result == True:
                    # status 0 校验成功。
                    return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {}})
                elif result == False:
                    # status 100 验证码hash值不匹配(包括验证码过期)。
                    return JsonResponse({"id": id, "status": 100, "message": "Error captcha hash", "data": {}})
                else:
                    # status -404 Unkown Error
                    return JsonResponse({"id": id, "status": -404, "message": "Unknown Error", "data": {}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class UserInfoView(View):
    def get(self, request, *args, **kwargs):
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
        if result == False:
            return JsonResponse({"id": -1, "status": -101, "message": "Error Token", "data": {}})
        data_dict = {"username": user.username, "name": user.last_name + user.first_name, "nickname": user.nickname,
                     "email": user.email, "phone": user.phone, "gender": user.gender}
        return JsonResponse({"id": -1, "status": 0, "message": "Successful", "data": data_dict})

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
        if type == "info":  ## 用户信息api
            if subtype == "get":
                if "username" in data.keys():
                    user = Users.objects.filter(username=data["username"])[0]
                data_dict = {"username": user.username, "name": user.last_name + user.first_name,
                             "nickname": user.nickname, "email": user.email, "phone": user.phone, "gender": user.gender}
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": data_dict})
            elif subtype == "update":  ## 用户信息更新api
                # 判断指定所需字段是否存在，若不存在返回status -1 json。
                for key in data.keys():
                    if key not in ["username", "phone", "name", "nickname", "email", "gender"]:
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return JsonResponse(
                            {"id": id, "status": -3, "message": "Error data key", "data": {}})
                if "username" in data.keys():
                    username = data["username"]
                    if user.username != username:
                        if user.is_superuser:
                            print("is superuser,update other user info")
                            user = Users.objects.filter(username=username)[0]
                            if user is None:
                                return JsonResponse({"id": id, "status": 100, "message": "No Such User", "data": {}})
                        else:
                            # status 102 没有权限进行操作
                            return JsonResponse(
                                {"id": id, "status": 102, "message": "No Permission Operation", "data": {}})
                for key in data.keys():
                    if key == "name":
                        if data["name"] == "":
                            first_name = ""
                            last_name = ""
                        else:
                            name = list(data[key])
                            last_name = name[0]
                            first_name = "".join(name[1:])
                        user.first_name = first_name
                        user.last_name = last_name
                    elif key == "nickname":
                        user.nickname = data[key]
                    elif key == "email":
                        user.email = data[key]
                    elif key == "gender":
                        if data[key] not in ["male", "female"]:
                            continue
                        else:
                            user.gender = data[key]
                    elif key == "phone":
                        continue
                try:
                    user.save()
                except Exception as e:
                    return JsonResponse({"id": id, "status": 101, "message": "Update UserInfo Failed"})

                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class PasswordView(View):
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
        # 处理json
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "password":
            if subtype == "forget":
                for key in ["username", "hash", "pass"]:
                    if key not in data.keys():
                        # status -3 data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                username = data["username"]
                hash = data["hash"]
                new_pass = data["pass"]
                redis_result = Redis.SafeCheck(hash=hash)
                if not redis_result:
                    # status -4 hash值错误
                    return JsonResponse({"id": id, "status": -4, "message": "Error hash", "data": {}})
                try:
                    user = Users.objects.get(username=username)
                except Exception as e:
                    # status 100 No such user 没有此用户
                    return JsonResponse({"id": id, "status": 100, "message": "No such user", "data": {}})
                user.set_password(new_pass)
                user.save()
                Tokens.objects.filter(user=user).delete()
                return JsonResponse({"id": id, "status": 0, "message": "successful", "data": {}})
            elif subtype == "change":
                for key in ["username", "old_pass", "new_pass"]:
                    if key not in data.keys():
                        # status -3 data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                username = data["username"]
                old_pass = data["old_pass"]
                new_pass = data["new_pass"]
                user = authenticate(request, username=username, password=old_pass)
                if user is None:
                    # 未查询到用户
                    # status 101 Error password
                    return JsonResponse({"id": id, "status": 100, "message": "Error username or password", "data": {}})
                user.set_password(new_pass)
                user.save()
                Tokens.objects.filter(user=user).delete()
                return JsonResponse({"id": id, "status": 0, "message": "successful", "data": {}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


class PortraitView(View):
    def get(self, request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        print("portrait ip - {}".format(ip))
        # return HttpResponse("{}".format(ip))
        try:
            username = request.GET.get("username")
            print("username:", username)
            if not username:
                with open(os.path.join(settings.MEDIA_ROOT, "users", "error.jpg"), "rb") as f:
                    img_data = f.read()
                return HttpResponse(img_data, content_type="image/jpg")
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            with open(os.path.join(settings.MEDIA_ROOT, "users", "error.jpg"), "rb") as f:
                img_data = f.read()
            return HttpResponse(img_data, content_type="image/jpg")
        user_list = Users.objects.filter(username=username)
        if len(user_list) == 1:
            file_name = MD5.md5(username) + ".user"
            try:
                with open(os.path.join(settings.MEDIA_ROOT, "users", file_name), "rb") as f:
                    img_data = f.read()
                return HttpResponse(img_data, content_type="image/jpg")
            except Exception as e:
                with open(os.path.join(settings.MEDIA_ROOT, "users", "default.jpg"), "rb") as f:
                    img_data = f.read()
                return HttpResponse(img_data, content_type="image/jpg")

        with open(os.path.join(settings.MEDIA_ROOT, "users", "error.jpg"), "rb") as f:
            img_data = f.read()
        return HttpResponse(img_data, content_type="image/jpg")

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
        data = dict(data["data"])
        ## -------正式处理事务-------
        if type == "portrait":
            if subtype == "upload":
                for key in ["base64"]:
                    if key not in data.keys():
                        # status -3 data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                img_base64 = str(data["base64"])
                base64_head_index = img_base64.find(";base64,")
                if base64_head_index != -1:
                    print("进行了替换")
                    img_base64 = img_base64.partition(";base64,")[2]
                file_name = MD5.md5(user.username) + ".user"
                # print("-------接收到数据-------\n", img_base64, "\n-------数据结构尾-------")
                try:
                    img_file = base64.b64decode(img_base64)
                except Exception as e:
                    return JsonResponse({"id": id, "status": 100, "message": "Error base64 data", "data": {}})
                # TODO 优化文件存储的效率（使用多线程），包括后期的人脸数据
                # TODO 后期对图片文件进行加密处理
                try:
                    with open(os.path.join(settings.MEDIA_ROOT, "users", file_name), "wb") as f:
                        f.write(img_file)
                except Exception as e:
                    return JsonResponse({"id": id, "status": 101, "message": "Upload portrait failed", "data": {}})
                user.image = "users/{}".format(file_name)
                user.save()
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {
                    "url": "/api/user/portrait/?username={}".format(user.username)}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
