from import_export.resources import ModelResource
from apps.rooms.models import Room, Hotel, Ambitus


class RoomResource(ModelResource):
    class Meta:
        model = Room


class HotelResource(ModelResource):
    class Meta:
        model = Hotel


class AmbitusResource(ModelResource):
    class Meta:
        model = Ambitus
