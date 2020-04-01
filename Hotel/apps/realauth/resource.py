from import_export.resources import ModelResource
from apps.realauth.models import RealAuth


class RealAuthResource(ModelResource):
    class Meta:
        model = RealAuth
