from import_export.resources import ModelResource
from apps.passengerFlow.models import PassengerFlow, PassengerFace


class PassengerFlowResource(ModelResource):
    class Meta:
        model = PassengerFlow


class PassengerFaceResource(ModelResource):
    class Meta:
        model = PassengerFace
