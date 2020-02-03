from Hotel import settings
import requests, json
from extral_apps import MD5

from datetime import datetime
import time
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

token = "2b750d4101e3ee20d551758a9cccb519"  # 13750687010
# token = "f5be3a953ffdfcb1bbe45d4379d05ade"  # 19857160634


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
#         "username": "13750687010",
#     }
# }
# # post 形式
# response = requests.post("http://127.0.0.1:8848/api/user/info/?token={}".format(token), data=json.dumps(data))
# # response = requests.post("https://hotel.lcworkroom.cn/api/user/info/?token={}".format(token), data=json.dumps(data))
# print(response.text)
# # get形式
# response = requests.get("http://127.0.0.1:8848/api/user/info/?token={}".format(token))
# # response = requests.get("https://hotel.lcworkroom.cn/api/user/info/?token={}".format(token))
# print(response.text)

# # 更新用户信息
# data = {
#     "id": 1234,
#     "type": "info",
#     "subtype": "update",
#     "data": {
#         "nickname": "FatBallFish",
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
#
# # 获取人员库信息
# data = {"id": 0,
#         "type": "group",
#         "subtype": "get",
#         "data": {"group_id": "5"}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/group/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/group/?token={}".format(token), data=json.dumps(data), headers=headers)
# print(response.text)
#
# # 获取人员库列表
# data = {"id": 0,
#         "type": "group",
#         "subtype": "list",
#         "data": {}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/group/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/group/?token={}".format(token), data=json.dumps(data), headers=headers)
# print(response.text)

# # 注册用户人脸
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "王凌超.jpg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "face",
#         "subtype": "register",
#         "data": {"base64": "{}".format(img_base64), "db": 1, "content": "我自己呐~"}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/?token={}".format(token), data=json.dumps(data), headers=headers)
# print(response.text)

# # 人脸查找
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "timg.jpg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "face",
#         "subtype": "find",
#         "data": {"base64": "{}".format(img_base64), "db": -1,"ret_type":0}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 人脸核验
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "14.jpg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "face",
#         "subtype": "verify",
#         "data": {"base64": "{}".format(img_base64), "ret_type": 0}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 实名认证
# data = {"id": 0,
#         "type": "realauth",
#         "subtype": "create",
#         "data": {
#             "id_type":"sfz",
#             "id":"33108219991127089X",
#             "name":"王凌超",
#             "gender":"male",
#             "birthday":time.mktime(time.strptime("2016-07-08","%Y-%m-%d")),
#             "organization":"临海市公安局"
#         }}
# response = requests.post(url="http://127.0.0.1:8848/api/realauth/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 更新实名认证
# data = {"id": 0,
#         "type": "realauth",
#         "subtype": "update",
#         "data": {
#             "organization":"临海市公安局"
#         }
#     }
# response = requests.post(url="http://127.0.0.1:8848/api/realauth/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 更新实名认证
# data = {"id": 0,
#         "type": "realauth",
#         "subtype": "get",
#         "data": {}
#         }
# # response = requests.post(url="http://127.0.0.1:8848/api/realauth/?token={}".format(token), data=json.dumps(data),
# #                          headers=headers)
# response = requests.post(url="https://hotel.lcworkroom.cn/api/realauth/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 设备注册
# data = {"id": 0, "type": "device", "subtype": "register",
#         "data": {"device_name": "测试设备", "device_content": "啦啦啦", "hotel_id": 1}}
# response = requests.post(url="http://127.0.0.1:8848/api/device/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# 设备登录
device_id = "ec26b6f7a55ec7013f7d6c84c2be8724"
data = {"id": 0, "type": "device", "subtype": "login", "data": {}}
response = requests.post(url="http://127.0.0.1:8848/api/device/login/?device_id={}".format(device_id),
                         data=json.dumps(data), headers=headers)
print(response.text)

# # 获取酒店列表
# data = {"id": 0, "type": "hotel", "subtype": "list", "data": {}}
# response = requests.post(url="http://127.0.0.1:8848/api/device/hotel/", data=json.dumps(data), headers=headers)
# print(response.text)
