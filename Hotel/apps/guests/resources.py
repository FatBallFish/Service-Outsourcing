from import_export.resources import ModelResource
from apps.guests.models import Guests, GuestRoom, GuestVisitor, Visitor, Orders


class GuestsResource(ModelResource):
    class Meta:
        model = Guests


class GuestRoomResource(ModelResource):
    class Meta:
        model = GuestRoom


class GuestVisitorResource(ModelResource):
    class Meta:
        model = GuestVisitor


class VisitorResource(ModelResource):
    class Meta:
        model = Visitor


class OrdersResource(ModelResource):
    class Meta:
        model = Orders
