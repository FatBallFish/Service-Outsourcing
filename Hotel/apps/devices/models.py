from django.db import models
from apps.users.models import BaseModel, Users
from apps.faces.models import FaceGroup


# Create your models here.

class Device(BaseModel):
    device_id = models.CharField(verbose_name="设备id", max_length=64, primary_key=True)
    device_name = models.CharField(verbose_name="设备名", max_length=30, unique=True)
    device_content = models.TextField(verbose_name="设备描述")

    class Meta:
        verbose_name = "设备信息"
        verbose_name_plural = verbose_name
        db_table = "devices"

    def __str__(self):
        return "{device}".format(device=self.device_name)


class DeviceGroup(BaseModel):
    faces_group = models.ForeignKey(verbose_name="人员库", to=FaceGroup, on_delete=models.CASCADE)
    device = models.ForeignKey(verbose_name="设备", to=Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "设备-人员库"
        verbose_name_plural = verbose_name
        db_table = "devices_faces_group"

    def __str__(self):
        return "{device}:{group}".format(device=self.device.device_name, group=self.faces_group.group_name)


class DeviceUser(BaseModel):
    user = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.CASCADE)
    device = models.ForeignKey(verbose_name="设备", to=Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "设备-用户"
        verbose_name_plural = verbose_name
        db_table = "devices_user"

    def __str__(self):
        return "{device}:{user}".format(user=self.user.username, device=self.device.device_name)


def DeviceDoki(device_id: str) -> object:
    device = Device.objects.filter(device_id=device_id)[0]
    if device is None:
        return False, ""
    return True, device


def GetBindDevice(user: object) -> list:
    deviceuser_list = DeviceUser.objects.filter(user=user)
    data_list = []
    for deviceuser in deviceuser_list:
        data_list.append(deviceuser.device)
    return data_list