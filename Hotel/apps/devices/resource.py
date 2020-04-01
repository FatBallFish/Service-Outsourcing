from import_export.resources import ModelResource
from apps.devices.models import Device, DeviceGroup


class DeviceResource(ModelResource):
    class Meta:
        model = Device


class DeviceGroupResource(ModelResource):
    class Meta:
        model = DeviceGroup