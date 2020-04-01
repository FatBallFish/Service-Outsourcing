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

# # 登录 - 密码
# data = {
#     "id": 1234,
#     "type": "login",
#     "subtype": "pass",
#     "data": {
#         "username": "13750687010",
#         "pass": "wlc570Q0",
#         "enduring": 1,
#     }
# }
# response = requests.post("http://127.0.0.1:8848/api/user/login/", data=json.dumps(data))
# # response = requests.post("https://hotel.lcworkroom.cn/api/user/login/", data=json.dumps(data))
# print(response.text)
# token = response.json()["data"]["token"]

# token = "59bc21b4e85cb1a4039802bd635294b9"  # 13750687010
# token = "f5be3a953ffdfcb1bbe45d4379d05ade"  # 19857160634
token = "8236f79ea096198bd7e3124a20816a26"  # 13858181317 艾
# token = "6a6f4be5aecd21636cf407cbaa8874cd"  # 13735866541 梁
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
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "img6.jpeg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "face",
#         "subtype": "find",
#         "data": {"base64": "{}".format(img_base64), "db": -1,"ret_type":1}}
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

# # 人脸特征数据获取 - 列表
# data = {"id": 0,
#         "type": "feature",
#         "subtype": "list",
#         "data": {"db": -1}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 人脸特征数据获取 - 单个
# data = {"id": 0,
#         "type": "feature",
#         "subtype": "get",
#         "data": {"ID":"33108219991127089X"}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 人脸口罩识别
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "14.jpg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "mask",
#         "subtype": "check",
#         "data": {"base64": "{}".format(img_base64)}}
# response = requests.post(url="http://127.0.0.1:8848/api/face/mask/?token={}".format(token), data=json.dumps(data),
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

# # 设备登录
# device_id = "ec26b6f7a55ec7013f7d6c84c2be8724"
# data = {"id": 0, "type": "device", "subtype": "login", "data": {}}
# response = requests.post(url="http://127.0.0.1:8848/api/device/login/?device_id={}".format(device_id),
#                          data=json.dumps(data), headers=headers)
# print(response.text)

# # 获取酒店列表
# data = {"id": 0, "type": "hotel", "subtype": "list", "data": {}}
# response = requests.post(url="http://127.0.0.1:8848/api/device/hotel/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 设备人脸特征数据获取 - 酒店
# device_id = "ec26b6f7a55ec7013f7d6c84c2be8724"
# data = {"id": 0,
#         "type": "feature",
#         "subtype": "hotel",
#         "data": {"hotel_id": 10}}
# response = requests.post(url="http://127.0.0.1:8848/api/device/feature/?device_id={}".format(device_id), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 设备人脸特征数据获取 - 设备
# device_id = "ec26b6f7a55ec7013f7d6c84c2be8724"
# data = {"id": 0,
#         "type": "feature",
#         "subtype": "device",
#         "data": {}}
# response = requests.post(url="http://127.0.0.1:8848/api/device/feature/?device_id={}".format(device_id), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 设备人脸特征数据获取 - 列表
# device_id = "ec26b6f7a55ec7013f7d6c84c2be8724"
# data = {"id": 0,
#         "type": "feature",
#         "subtype": "list",
#         "data": {"db": -1}}
# response = requests.post(url="http://127.0.0.1:8848/api/device/feature/?device_id={}".format(device_id), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)
#
# # 设备人脸特征数据获取 - 单个
# data = {"id": 0,
#         "type": "feature",
#         "subtype": "get",
#         "data": {"ID":"33108219991127089X"}}
# response = requests.post(url="http://127.0.0.1:8848/api/device/feature/?device_id={}".format(device_id), data=json.dumps(data),
#                          headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 获取三级联动
# data = {"keywords": "浙江", "subdistrict": 1}
# response = requests.get(url="http://127.0.0.1:8848/api/map/district/", params=data)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)


# # 图片上传 - COS
# with open(os.path.join(settings.BASE_DIR, "media", "tmp", "14.jpg"), "rb") as f:
#     file_data = f.read()
# # print(file_data)
# img_base64 = str(base64.b64encode(file_data), "utf-8")
# print("base64:\n{}".format(img_base64))
# data = {"id": 0,
#         "type": "pic",
#         "subtype": "upload",
#         "data": {"name": "13750687010", "content": "我的头像", "type": "jpg", "upload_to": "users", "if_local": False,
#                  "base64": "{}".format(img_base64)}}
# response = requests.post(url="http://127.0.0.1:8848/api/pic/", data=json.dumps(data), headers=headers)
# # response = requests.post(url="https://hotel.lcworkroom.cn/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

# # 站内信，是否有新消息
# data = {"id": 0, "type": "msg", "subtype": "has_new", "data": {}}
# response = requests.post(url="http://127.0.0.1:8848/api/msg/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# 站内信，获取系统通知
# data = {"id": 0, "type": "msg", "subtype": "sys", "data": {"if_new": 2}}
# response = requests.post(url="http://127.0.0.1:8848/api/msg/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 站内信，标记已读状态
# data = {"id": 0, "type": "msg", "subtype": "sign",
#         "data": {"msg_id": 1}}
# response = requests.post(url="http://127.0.0.1:8848/api/msg/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 站内信，获取私聊通知
# data = {"id": 0, "type": "msg", "subtype": "private",
#         "data": {"if_new": 2, "people": "13750687010", "start": 0, "limit": -1}}
# response = requests.post(url="http://127.0.0.1:8848/api/msg/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 站内信，发送私聊通知
# data = {"id": 0, "type": "msg", "subtype": "send",
#         "data": {"receiver": "13750687010", "title": "回复", "content": "你也好呀！"}}
# response = requests.post(url="http://127.0.0.1:8848/api/msg/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 站内信，筛选
# data = {"id": 0, "type": "msg", "subtype": "filter",
#         "data": {"type": "system", "subtype": "", "if_new": 1}}
# response = requests.post(url="http://127.0.0.1:8848/api/msg/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 站内信，批量已读
# data = {"id": 0, "type": "msg", "subtype": "sign_batch",
#         "data": {"sys": 0}}
# response = requests.post(url="http://127.0.0.1:8848/api/msg/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 站内信，获取私聊列表
# data = {"id": 0, "type": "msg", "subtype": "msg_list", "data": {}}
# response = requests.post(url="http://127.0.0.1:8848/api/msg/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 寄存柜，申请寄存柜
# data = {"id": 0, "type": "locker", "subtype": "apply", "data": {"order_id": 4}}
# response = requests.post(url="http://127.0.0.1:8848/api/locker/apply/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 寄存柜，取消寄存柜
# data = {"id": 0, "type": "locker", "subtype": "cancel", "data": {"apply_id": 4}}
# response = requests.post(url="http://127.0.0.1:8848/api/locker/apply/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 寄存柜，获取寄存列表
# data = {"id": 0, "type": "locker", "subtype": "list", "data": {"order_id": 4}}
# response = requests.post(url="http://127.0.0.1:8848/api/locker/info/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)
#
# # 寄存柜，获取单个寄存信息
# data = {"id": 0, "type": "locker", "subtype": "get", "data": {"apply_id": 4}}
# response = requests.post(url="http://127.0.0.1:8848/api/locker/info/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# # 寄存柜，核验预约信息
# data = {"id": 0, "type": "locker", "subtype": "get", "data": {"apply_id": 4}}
# response = requests.post(url="http://127.0.0.1:8848/api/locker/info/?token={}".format(token), data=json.dumps(data),
#                          headers=headers)
# print(response.text)

# 寄存柜，核验预约信息
data = {"id": 0, "type": "locker", "subtype": "get", "data": {"apply_id": 4}}
response = requests.post(url="http://127.0.0.1:8848/api/table/test/", data=json.dumps(data),
                         headers=headers)
print(response.text)
