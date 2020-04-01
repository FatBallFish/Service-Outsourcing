from import_export.resources import ModelResource
from apps.msg.models import Messages, MessageText, MessageSysStatus


class MessagesResource(ModelResource):
    class Meta:
        model = Messages


class MessageTextResource(ModelResource):
    class Meta:
        model = MessageText


class MessageSysStatusResource(ModelResource):
    class Meta:
        model = MessageSysStatus
