from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.db.models import Q
from Hotel import settings

from apps.users.models import Users
from apps.tokens.models import Tokens, Doki2
from apps.faces.models import FaceData
from apps.realauth.models import RealAuth
from apps.pics.models import PicBed
from extral_apps import MD5
from extral_apps.m_redis import py_redis as Redis
from extral_apps.m_img import py_captcha_main as ImgCaptcha
from extral_apps.m_sms import py_sms_main as SmsCaptcha
from extral_apps.m_cos import py_cos_main as COS
from extral_apps.m_arcface import main as Arcface
from extral_apps.m_hpsocket import main as HPSocket
from extral_apps.m_facemask import main as FaceMask
from datetime import datetime, timedelta
import json, base64, random
import os, time

# Create your views here.
COS.Initialize(settings.BASE_DIR)
Redis.Initialize(settings.BASE_DIR)
ImgCaptcha.Initialize(settings.BASE_DIR)
SmsCaptcha.Initialize(settings.BASE_DIR)
Arcface.Initialize(False)
HPSocket.Initialize(settings.BASE_DIR)
FaceMask.Initialize(settings.BASE_DIR)

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
                try:
                    Users.objects.get(username=username)
                except Exception as e:
                    # status 100 用户不存在
                    json_dict = {"id": id, "status": 100, "message": "No such user", "data": {}}
                    return JsonResponse(json_dict)
                # 判断用户是否是以短信验证码形式注册
                user_check = authenticate(request, username=username, password=username)
                if user_check is not None:
                    # status 101 用户密码未设置
                    json_dict = {"id": id, "status": 101, "message": "Password not set", "data": {}}
                    return JsonResponse(json_dict)
                # 检验账号密码正确性
                user = authenticate(request, username=username, password=password)
                if user is None:
                    # status 102 用户密码错误
                    json_dict = {"id": id, "status": 102, "message": "Error password", "data": {}}
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
            elif subtype == "sms":
                for key in data.keys():
                    if key not in ["username", "hash", "enduring"]:
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                username = data["username"]
                hash = data["hash"]
                if "enduring" in data.keys():
                    enduring = data["enduring"]
                    if not isinstance(enduring, int):
                        enduring = 0
                    if enduring != 0:
                        enduring = 1
                else:
                    # enduring字段未传入，默认为假
                    enduring = 0
                hash_result = Redis.SafeCheck(hash=hash)
                if not hash_result:
                    # status -4 hash不存在
                    return JsonResponse({"id": id, "status": -4, "message": "Error hash", "data": {}})

                try:
                    user = Users.objects.get(username=username)
                    login_type = "login"
                except Exception as e:
                    # 用户不存在，即将创建
                    try:
                        user = Users.objects.create_user(username=username, password=username, phone=username)
                        login_type = "create"
                    except Exception as e:
                        # status 100 用户不存在
                        return JsonResponse({"id": id, "status": 100, "message": "Create User Failed", "data": {}})
                login_user_nopass(request=request, user=user)
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
                return JsonResponse({"id": id, "status": 0, "message": "Successful",
                                     "data": {"token": token, "login_type": login_type}})
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
            if subtype == "generate":
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
                elif command_type == 3:
                    # 找回密码
                    result = SmsCaptcha.SendCaptchaCode(phone_number=phone, captcha=code, command_str="账号登录",
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
        print("result:{},user:{}".format(result, user))
        if result == False:
            return JsonResponse({"id": -1, "status": -101, "message": "Error Token", "data": {}})
        real_auth_ID = None
        if user.real_auth:
            real_auth_ID = user.real_auth.ID
        if_face = False
        if user.face:
            if_face = True
        data_dict = {"id": user.id, "username": user.username, "nickname": user.nickname, "email": user.email,
                     "phone": user.phone, "ID": real_auth_ID, "if_face": if_face}
        print(data_dict)
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
                    username = data['username']
                    try:
                        user = Users.objects.get(username=username)
                    except Exception as e:
                        return JsonResponse({"id": id, "status": 100, "message": "No Such User", "data": {}})
                # 若username字段不存在，则自动使用Doki函数获取的user值
                real_auth_ID = None
                if user.real_auth:
                    real_auth_ID = user.real_auth.ID
                data_dict = {"id": user.id, "username": user.username, "nickname": user.nickname, "email": user.email,
                             "phone": user.phone, "ID": real_auth_ID}
                print(data_dict)
                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": data_dict})
            elif subtype == "update":  ## 用户信息更新api
                # 判断指定所需字段是否存在，若不存在返回status -1 json。
                for key in data.keys():
                    if key not in ["username", "phone", "nickname", "email", "face_id", "real_auth_id"]:
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                if "username" in data.keys():
                    username = data["username"]
                    if user.username != username:
                        if user.is_superuser:
                            print("is superuser,update other user info")
                            try:
                                user = Users.objects.get(username=username)
                            except Exception as e:
                                return JsonResponse({"id": id, "status": 100, "message": "No Such User", "data": {}})
                        else:
                            # status 102 没有权限进行操作
                            return JsonResponse(
                                {"id": id, "status": 102, "message": "No Permission Operation", "data": {}})
                for key in data.keys():
                    if key == "nickname":
                        user.nickname = data[key]
                    elif key == "email":
                        user.email = data[key]
                    elif key == "phone":
                        continue
                    elif key == "face_id":
                        if data[key] is None or data[key] == "":
                            user.face = None
                        else:
                            face_id = data[key]
                            try:
                                face = FaceData.objects.get(ID=face_id)
                                user.face = face
                            except Exception as e:
                                return JsonResponse({"id": id, "status": 103, "message": "No Such Face", "data": {}})
                    elif key == "real_auth_id":
                        if data[key] is None or data[key] == "":
                            user.real_auth = None
                        else:
                            real_auth_ID = str(data[key])
                            try:
                                real_auth = RealAuth.objects.get(ID=real_auth_ID)
                                user.real_auth = real_auth
                            except Exception as e:
                                return JsonResponse(
                                    {"id": id, "status": 104, "message": "No Such RealAuth", "data": {}})
                # 额外的判断与处理
                if user.real_auth is None:
                    user.face = None
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


class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        try:
            param_dict = request.GET
            print(param_dict)
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        data_list = []
        if "user_id" in param_dict:
            user_id = str(param_dict["user_id"])
            try:
                user = Users.objects.get(username=user_id)
            except Exception as e:
                return JsonResponse(
                    {"id": -1, "status": 0, "message": "Successful",
                     "data": {"num": len(data_list), "list": data_list}})
            data_dict = {"user_id": user.username, "nickname": user.nickname}
            data_list.append(data_dict)
        elif "keywords" in param_dict:
            keywords = str(param_dict["keywords"])
            user_list = Users.objects.filter(Q(nickname__contains=keywords) | Q(username=keywords))
            for user in user_list:
                data_dict = {"user_id": user.username, "nickname": user.nickname}
                data_list.append(data_dict)
        return JsonResponse(
            {"id": -1, "status": 0, "message": "Successful", "data": {"num": len(data_list), "list": data_list}})


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
                # 判断用户是否存在
                try:
                    user = Users.objects.get(username=username)
                except Exception as e:
                    # status 100 No such user 没有此用户
                    return JsonResponse({"id": id, "status": 100, "message": "No such user", "data": {}})
                # 判断用户是否是以短信验证码形式注册
                user_check = authenticate(request, username=username, password=username)
                if user_check is not None:
                    # status 101 用户密码未设置
                    json_dict = {"id": id, "status": 101, "message": "Password not set", "data": {}}
                    return JsonResponse(json_dict)
                redis_result = Redis.SafeCheck(hash=hash)
                if not redis_result:
                    # status -4 hash值错误
                    return JsonResponse({"id": id, "status": -4, "message": "Error hash", "data": {}})

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
                # 判断用户是否存在
                try:
                    Users.objects.get(username=username)
                except Exception as e:
                    # status 100 No such user 没有此用户
                    return JsonResponse({"id": id, "status": 100, "message": "No such user", "data": {}})
                # 判断用户是否是以短信验证码形式注册
                user_check = authenticate(request, username=username, password=username)
                if user_check is not None:
                    # status 101 用户密码未设置
                    json_dict = {"id": id, "status": 101, "message": "Password not set", "data": {}}
                    return JsonResponse(json_dict)
                # 验证账号密码正确性
                user = authenticate(request, username=username, password=old_pass)
                if user is None:
                    # status 102 Error password
                    return JsonResponse({"id": id, "status": 102, "message": "Error password", "data": {}})
                if new_pass == username:
                    # status 103 用户密码不能与账号一致
                    json_dict = {"id": id, "status": 103, "message": "Password cannot be the same as account",
                                 "data": {}}
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
                return HttpResponseRedirect("/media/users/error.jpg")
                # with open(os.path.join(settings.MEDIA_ROOT, "users", "error.jpg"), "rb") as f:
                #     img_data = f.read()
                # return HttpResponse(img_data, content_type="image/jpg")
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return HttpResponseRedirect("/media/users/error.jpg")
            # with open(os.path.join(settings.MEDIA_ROOT, "users", "error.jpg"), "rb") as f:
            #     img_data = f.read()
            # return HttpResponse(img_data, content_type="image/jpg")

        try:
            Users.objects.get(username=username)
            return HttpResponseRedirect("/api/pic/get/users/?name={}".format(username))
            # file_name = MD5.md5(username) + ".user"
            # try:
            #     with open(os.path.join(settings.MEDIA_ROOT, "users", file_name), "rb") as f:
            #         img_data = f.read()
            #     return HttpResponse(img_data, content_type="image/jpg")
            # except Exception as e:
            #     with open(os.path.join(settings.MEDIA_ROOT, "users", "default.jpg"), "rb") as f:
            #         img_data = f.read()
            #     return HttpResponse(img_data, content_type="image/jpg")
        except Exception as e:
            return HttpResponseRedirect("/media/users/error.jpg")
            # with open(os.path.join(settings.MEDIA_ROOT, "users", "error.jpg"), "rb") as f:
            #     img_data = f.read()
            # return HttpResponse(img_data, content_type="image/jpg")

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
                img_type = "user"
                if_local = False
                if "if_local" in data.keys():
                    if_local = data["if_local"]
                    if not isinstance(if_local, bool):
                        if_local = False
                md5 = MD5.md5("users" + user.username)
                pic_name = md5 + "." + img_type
                file_name = os.path.join("users", pic_name)
                # print("-------接收到数据-------\n", img_base64, "\n-------数据结构尾-------")
                try:
                    img_file = base64.b64decode(img_base64)
                except Exception as e:
                    return JsonResponse({"id": id, "status": 100, "message": "Error base64 data", "data": {}})

                if if_local:
                    result, url = LocalWrite(file_name, img_file)
                else:
                    result, url = CosWrite(file_name, img_file)
                local_url = None
                cos_url = None
                if result:
                    if if_local:
                        local_url = url
                        user.image = url
                        url = "/media/" + url
                    else:
                        user.image = url
                        cos_url = url
                else:
                    if if_local:
                        # status -600 本地上传失败
                        return JsonResponse({"id": id, "status": -600, "message": "Local upload Error", "data": {}})
                    else:
                        # status -500 本地上传失败
                        return JsonResponse({"id": id, "status": -500, "message": "COS upload Error", "data": {}})
                defaults = {"content": "", "md5": md5, "if_local": if_local, "local_url": local_url,
                            "cos_url": cos_url}
                PicBed.objects.update_or_create(defaults=defaults, name=user.username, upload_to="users")
                user.save()

                return JsonResponse({"id": id, "status": 0, "message": "Successful", "data": {
                    "url": url}})
            else:
                # status -2 json的value错误。
                return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})
        else:
            # status -2 json的value错误。
            return JsonResponse({"id": id, "status": -2, "message": "Error JSON value", "data": {}})


def login_user_nopass(request, user):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    from django.contrib.auth import login
    return login(request, user)


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
