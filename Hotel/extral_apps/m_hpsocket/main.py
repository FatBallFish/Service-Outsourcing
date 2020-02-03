# coding: utf-8
from Hotel import settings
from apps.devices.models import Device, DeviceGroup
from apps.faces.models import FaceData, FaceGroup
from apps.users.models import Users

from extral_apps import MD5
from extral_apps.m_arcface import main as Arcface

import time, sys, os
from HPSocket import TcpPack
from HPSocket import helper
import HPSocket.pyhpsocket as HPSocket
import json, base64


def Initialize(main_path: str):
    """
    HP-Socket 初始化
    :param main_path: 程序主目录地址
    """
    global svr
    svr = Server()
    svr.Start(host="0.0.0.0", port=settings.HP_SOCKET_PORT, head_flag=settings.HP_SOCKET_FLAG,
              size=settings.HP_SOCKET_MAXSIZE)

    global Main_filepath
    Main_filepath = main_path
    print("[HPSocket] Module HPSocket loaded")
    # sys.path.append(main_path)
    # sys.path.append(os.getcwd() + '/../')


class Server(TcpPack.HP_TcpPackServer):
    EventDescription = TcpPack.HP_TcpPackServer.EventDescription
    conn_pool = {}

    @EventDescription
    def OnAccept(self, Sender, ConnID, Client):
        (ip, port) = HPSocket.HP_Server_GetRemoteAddress(Sender=Sender, ConnID=ConnID)
        self.conn_pool.setdefault(ConnID, [ip, port, ""])
        print('[%d, OnAccept] < %s' % (ConnID, (ip, port)))

    @EventDescription
    def OnSend(self, Sender, ConnID, Data):
        print('[%d, OnSend] > %s' % (ConnID, repr(Data)))

    @EventDescription
    def OnReceive(self, Sender, ConnID, Data):
        print('[%d, OnReceive] < %s' % (ConnID, Data.decode()))
        try:
            data = json.loads(Data.decode())
        except Exception as e:
            json_str = json.dumps({"id": -1, "status": -1, "message": "Error JSON key", "data": {}})
            self.Send(Sender=Sender, ConnID=ConnID, Data=json_str.encode("utf8"))
            return HPSocket.EnHandleResult.HR_OK
        id = data["id"]
        if "id" in data.keys():
            id = data["id"]
        else:
            id = -1
            # 判断指定所需字段是否存在，若不存在返回status -1 json。
        for key in ["type", "subtype", "data"]:
            if key not in data.keys():
                # status -1 json的key错误。
                json_dict = {"id": id, "status": -1, "message": "Error JSON key", "data": {}}
                self.Send(Sender=Sender, ConnID=ConnID, Data=json.dumps(json_dict))
                return HPSocket.EnHandleResult.HR_OK
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "login":
            if subtype == "login":
                ret_data = self.request_login(id=id, ConnID=ConnID, data=data)
                self.Send(Sender=Sender, ConnID=ConnID, Data=ret_data)
                return HPSocket.EnHandleResult.HR_OK
            else:
                # status -2 json的value错误。
                return json.dumps({"id": id, "status": -2, "message": "Error JSON value", "data": {}}).encode("utf8")
        elif type == "face":
            if subtype == "verify":
                ret_data = self.request_face_verify(id=id, ConnID=ConnID, data=data)
                self.Send(Sender=Sender, ConnID=ConnID, Data=ret_data)
                return HPSocket.EnHandleResult.HR_OK

        # self.Send(Sender=Sender, ConnID=ConnID, Data=Data)
        return HPSocket.EnHandleResult.HR_OK

    # @EventDescription
    def OnClose(self, Sender, ConnID, Operation, ErrorCode):
        (ip, port) = HPSocket.HP_Server_GetRemoteAddress(Sender=Sender, ConnID=ConnID)
        print('[%d, OnClose] > %s opt=%d err=%d' % (ConnID, (ip, port), Operation, ErrorCode))
        try:
            device_id = self.conn_pool.get(ConnID)[2]
            device = Device.objects.get(device_id=device_id)
            device.is_online = False
            device.save()
        except Exception as e:
            print("get device failed")
        try:
            self.conn_pool.pop(ConnID)
        except Exception as e:
            print("pop '{}' failed".format(ConnID))

        return HPSocket.EnHandleResult.HR_OK

    def request_login(self, ConnID, data: dict, id: int = -1) -> bytes:
        if "device_id" not in data.keys():
            return json.dumps({"id": id, "status": -3, "message": "Error data key", "data": {}}).encode("utf8")
        device_id = data["device_id"]
        try:
            device = Device.objects.get(device_id=device_id)
        except:
            # status 100 错误的设备id
            return json.dumps({"id": id, "status": 100, "message": "Error device_id", "data": {}}).encode("utf8")
        device.is_online = True
        device.save()
        self.conn_pool[ConnID][2] = device_id
        return json.dumps({"id": id, "status": 0, "message": "Successful", "data": {}}).encode("utf8")

    def request_face_verify(self, ConnID, data: dict, id: int = -1) -> bytes:
        for key in ["phone", "base64"]:
            if key not in data.keys():
                # status -3 json的value错误。
                return json.dumps({"id": id, "status": -3, "message": "Error data key", "data": {}}).encode("utf8")
        phone = str(data["phone"])
        try:
            user = Users.objects.get(username=phone)
        except Exception as e:
            # status 99 错误的手机号
            return json.dumps({"id": id, "status": 99, "message": "Error phone", "data": {}}).encode("utf8")
        if not user.face:
            # status 100 人脸未认证 No authentication
            return json.dumps({"id": id, "status": 100, "message": "No face authentication", "data": {}}).encode("utf8")

        img_base64 = data["base64"]
        base64_head_index = img_base64.find(";base64,")
        if base64_head_index != -1:
            print("进行了替换")
            img_base64 = img_base64.partition(";base64,")[2]

        img_type = "face"
        img_file = base64.b64decode(img_base64)
        pic_name = MD5.md5_bytes(img_file) + "." + img_type
        file_name = os.path.join(settings.BASE_DIR, "media", "tmp", pic_name)
        # print(file_name)
        # todo 优化本地存储性能
        with open(file_name, "wb") as f:
            f.write(img_file)
        # Arcface.reload_features(db=db)
        json_dict = Arcface.checkFace(file_name, user=user)
        if os.path.exists(file_name):
            os.remove(file_name)
        num = json_dict["num"]
        data_list = json_dict["list"]
        if num == 0:
            # if not json_dict:
            # status 101 图片中无人脸数据
            return json.dumps({"id": id, "status": 101, "message": "No face data in base64", "data": {}}).encode("utf8")
        elif num != 1:
            # status 102 图片中人脸数据过多
            return json.dumps(
                {"id": id, "status": 102, "message": "Too much face data in base64", "data": {}}).encode("utf8")
        ret_type = 0
        if "ret_type" in data.keys():
            if isinstance(data["ret_type"], str):
                if str(data["ret_type"]).isdecimal():
                    ret_type = int(data["ret_type"])
            elif isinstance(data["ret_type"], int):
                ret_type = data["ret_type"]
            else:
                ret_type = 0
        face_dict = data_list[0]
        ID = face_dict["ID"]
        liveness = face_dict["liveness"]
        threshold = face_dict["threshold"]
        check_result = True if ID == user.face.ID else False
        sample_dict = {"result": check_result, "ID": ID, "liveness": liveness, "threshold": threshold}
        if ret_type == 0:  # 简略返回，result，liveness，threshold
            return json.dumps({"id": id, "status": 0, "message": "successful",
                               "data": sample_dict}).encode("utf8")
        else:
            face_dict["result"] = check_result
            # status 0 successful
            return json.dumps({"id": id, "status": 0, "message": "successful", "data": face_dict}).encode("utf8")


if __name__ == '__main__':
    svr = Server()
    svr.Start(host='0.0.0.0', port=9527, head_flag=1023)
