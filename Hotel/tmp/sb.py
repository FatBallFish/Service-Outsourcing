from Hotel import settings
import requests, json
import base64, os

headers = {"content-type": "application/json"}
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
# response = requests.post(url="http://127.0.0.1:8080/api/face/register/", data=json.dumps(data), headers=headers)
# print(response.text)

## 查询人脸
with open(os.path.join(settings.BASE_DIR, "media", "tmp", "吴雨欣.jpeg"), "rb") as f:
    file_data = f.read()
# print(file_data)
img_base64 = str(base64.b64encode(file_data), "utf-8")
print("base64:\n{}".format(img_base64))
data = {"id": 0,
        "type": "check",
        "subtype": "facedata",
        "data": {"base64": "{}".format(img_base64)}}
response = requests.post(url="http://127.0.0.1:8080/api/face/register/", data=json.dumps(data), headers=headers)
print(response.text)
