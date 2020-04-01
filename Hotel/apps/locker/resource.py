from import_export.resources import ModelResource
from apps.locker.models import LockerOrder, Locker


class LockerResource(ModelResource):
    model = Locker


class LockerOrderResource(ModelResource):
    class Meta:
        model = LockerOrder
