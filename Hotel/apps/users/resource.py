from import_export.resources import ModelResource
from apps.users.models import Users


class UsersResource(ModelResource):
    class Meta:
        model = Users
