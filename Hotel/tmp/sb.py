from Hotel import settings
import requests, json
from extral_apps import MD5

import base64, os

headers = {"content-type": "application/json"}
# # 发送手机短信
# data = {"id": 0, "status": 0, "type": "sms", "subtype": "generate", "data": {"phone": "19857160634"}}
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/captcha/",data=json.dumps(data),headers=headers)
# response = requests.post(url="http://localhost:8848/api/captcha/", data=json.dumps(data), headers=headers)
# print(response.text)
# code = input("验证码：")
# rand = input("随机值：")
# md5 = MD5.md5(code, rand)
# print("md5:", md5)
# # 注册
# # md5 = "dbf1b8bee48178556a28c4fcb2921340"
# data = {"id": 0, "status": 0, "type": "register", "subtype": "phone",
#         "data": {"username": "19857160634", "hash": md5, "pass": "wlc570Q0"}}
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/user/register/",data=json.dumps(data),headers=headers)
# response = requests.post(url="http://localhost:8848/api/user/register/", data=json.dumps(data), headers=headers)
# print(response.text)


# 登录
data = {
    "id": 1234,
    "type": "login",
    "subtype": "pass",
    "data": {
        "username": "19857160634",
        "pass": "wlc570Q0",
        "enduring": 0,
    }
}
# response = requests.post("http://localhost:8848/api/user/login/", data=json.dumps(data))
response = requests.post("https://hotel.lcworkroom.cn/api/user/login/", data=json.dumps(data))
print(response.text)
token = response.json()["data"]["token"]
# Doki
# response = requests.get("http://localhost:8848/api/user/doki/?token={}".format(token))
response = requests.get("https://hotel.lcworkroom.cn/api/user/doki/?token={}".format(token))
print(response.text)
# response = requests.post("http://localhost:8848/api/user/doki/?token={}".format(token))
response = requests.post("https://hotel.lcworkroom.cn/api/user/doki/?token={}".format(token))
print(response.text)
# 获取用户信息
data = {
    "id": 1234,
    "type": "info",
    "subtype": "get",
    "data": {
        "username": "19857160634",
    }
}
# post 形式
# response = requests.post("http://localhost:8848/api/user/info/?token={}".format(token), data=json.dumps(data))
response = requests.post("http://hotel.lcworkroom.cn/api/user/info/?token={}".format(token), data=json.dumps(data))
print(response.text)
# get形式
# response = requests.get("http://localhost:8848/api/user/info/?token={}".format(token))
response = requests.get("http://hotel.lcworkroom.cn/api/user/info/?token={}".format(token))
print(response.text)

# # 更新用户信息
# data = {
#     "id": 1234,
#     "type": "info",
#     "subtype": "update",
#     "data": {
#         "username": "19857160634",
#         "name": "王凌超",
#         "gender": "male",
#         "email":"893721708@qq.com"
#     }
# }
# response = requests.post("http://localhost:8848/api/user/info/?token={}".format(token), data=json.dumps(data))
# print(response.text)


# # 新建用户人脸库
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "吴雨欣.jpeg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "register",
#         "subtype": "facedata",
#         "data": {"base64": "{}".format(img_base64), "name": "吴雨欣", "faces_group_id": 1,"content":"我最爱的人呐"}}
# # response = requests.post(url="http://127.0.0.1:8080/api/face/register/", data=json.dumps(data), headers=headers)
# response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 查询人脸
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "19.jpeg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "check",
#         "subtype": "facedata",
#         "data": {"base64": "{}".format(img_base64)}}
# # response = requests.post(url="http://127.0.0.1:8080/api/face/register/", data=json.dumps(data), headers=headers)
# response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)
