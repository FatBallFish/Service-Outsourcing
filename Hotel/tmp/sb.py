from Hotel import settings
import requests, json
from extral_apps import MD5

import base64, os

headers = {"content-type": "application/json"}

# # 发送手机短信
# data = {"id": 0, "status": 0, "type": "sms", "subtype": "generate",
#         "data": {"phone": "13750687010", "command_type": 3}}
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/captcha/",data=json.dumps(data),headers=headers)
# response = requests.post(url="http://127.0.0.1:8848/api/captcha/", data=json.dumps(data), headers=headers)
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
# response = requests.post(url="http://127.0.0.1:8848/api/user/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 登录 - 短信
# data = {
#     "id": 1234,
#     "type": "login",
#     "subtype": "sms",
#     "data": {
#         "username": "13750687010",
#         "hash": md5,
#         "enduring": 1,
#     }
# }
# response = requests.post("http://127.0.0.1:8848/api/user/login/", data=json.dumps(data))
# # response = requests.post("https://hotel.lcworkroom.cn/api/user/login/", data=json.dumps(data))
# print(response.text)
# token = response.json()["data"]["token"]

# 登录 - 密码
# data = {
#     "id": 1234,
#     "type": "login",
#     "subtype": "pass",
#     "data": {
#         "username": "123",
#         "pass": "wlc570Q0123",
#         "enduring": 1,
#     }
# }
# response = requests.post("http://127.0.0.1:8848/api/user/login/", data=json.dumps(data))
# # response = requests.post("https://hotel.lcworkroom.cn/api/user/login/", data=json.dumps(data))
# print(response.text)
# token = response.json()["data"]["token"]

token = "7e5758432106806d1c98d2aa6c803483"  # 13750687010

# # Doki - GET模式
# response = requests.get("http://127.0.0.1:8848/api/user/doki/?token={}".format(token))
# # response = requests.get("https://hotel.lcworkroom.cn/api/user/doki/?token={}".format(token))
# print(response.text)
# # Doki - POST模式
# response = requests.post("http://127.0.0.1:8848/api/user/doki/?token={}".format(token))
# # response = requests.post("https://hotel.lcworkroom.cn/api/user/doki/?token={}".format(token))
# print(response.text)
# # 获取用户信息
# data = {
#     "id": 1234,
#     "type": "info",
#     "subtype": "get",
#     "data": {
#         "username": "123",
#     }
# }
# # post 形式
# # response = requests.post("http://127.0.0.1:8848/api/user/info/?token={}".format(token), data=json.dumps(data))
# response = requests.post("https://hotel.lcworkroom.cn/api/user/info/?token={}".format(token), data=json.dumps(data))
# print(response.text)
# get形式
# response = requests.get("http://127.0.0.1:8848/api/user/info/?token={}".format(token))
# response = requests.get("https://hotel.lcworkroom.cn/api/user/info/?token={}".format(token))
# print(response.text)

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
# response = requests.post("http://127.0.0.1:8848/api/user/info/?token={}".format(token), data=json.dumps(data))
# print(response.text)

# # 修改密码
# data = {
#     "id": 1234,
#     "type": "password",
#     "subtype": "change",
#     "data": {
#         "username": "19857160634",
#         "old_pass": "wlc570Q0",
#         "new_pass": "wlc570Q0123",
#     }
# }
# response = requests.post("http://127.0.0.1:8848/api/user/password/", data=json.dumps(data))
# # response = requests.post("https://hotel.lcworkroom.cn/api/user/password/", data=json.dumps(data))
# print(response.text)

# # 更新头像
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "14.jpg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "portrait",
#         "subtype": "upload",
#         "data": {"base64": "{}".format(img_base64)}}
# response = requests.post(url="http://127.0.0.1:8848/api/user/portrait/?token={}".format(token), data=json.dumps(data), headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/user/portrait/?token={}".format(token), data=json.dumps(data), headers=headers)
# print(response.text)

# # 新建人员库
# data = {"id": 0,
#         "type": "group",
#         "subtype": "create",
#         "data": {"group_name": "西和6幢人员库", "group_content": "浙江科技学院西和公寓6幢人脸数据库"}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/group/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/group/?token={}".format(token), data=json.dumps(data), headers=headers)
# print(response.text)

# # 更新人员库
# data = {"id": 0,
#         "type": "group",
#         "subtype": "update",
#         "data": {"group_name": "西和5幢人员库", "group_content": "浙江科技学院西和公寓5幢人脸数据库"}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/group/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/group/?token={}".format(token), data=json.dumps(data), headers=headers)
# print(response.text)

# # 删除人员库
# data = {"id": 0,
#         "type": "group",
#         "subtype": "delete",
#         "data": {"group_name": "西和5幢人员库"}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/group/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/group/?token={}".format(token), data=json.dumps(data), headers=headers)
# print(response.text)

# 获取人员库信息
data = {"id": 0,
        "type": "group",
        "subtype": "get",
        "data": {"group_id": "5"}}
response = requests.post(url="http://127.0.0.1:8848/api/face/group/?token={}".format(token), data=json.dumps(data),
                         headers=headers)
# response = requests.post(url="https://hotel.lcworkroom.cn/api/face/group/?token={}".format(token), data=json.dumps(data), headers=headers)
print(response.text)

# 获取人员库列表
data = {"id": 0,
        "type": "group",
        "subtype": "list",
        "data": {}}
response = requests.post(url="http://127.0.0.1:8848/api/face/group/?token={}".format(token), data=json.dumps(data),
                         headers=headers)
# response = requests.post(url="https://hotel.lcworkroom.cn/api/face/group/?token={}".format(token), data=json.dumps(data), headers=headers)
print(response.text)

# # 注册用户人脸
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "某某某.jpeg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "register",
#         "subtype": "facedata",
#         "data": {"base64": "{}".format(img_base64), "name": "某某某", "faces_group_id": 1,"content":"123"}}
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
