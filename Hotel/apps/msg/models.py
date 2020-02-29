from django.db import models
from django.db.models import Q
from django.utils.html import format_html

from apps.users.models import BaseModel, Users


# Create your models here.
class MessageText(BaseModel):
    title = models.CharField(verbose_name="标题", max_length=100)
    content = models.TextField(verbose_name="内容", null=True, blank=True)

    def __str__(self):
        return "{}({})".format(self.title, self.id)

    class Meta:
        verbose_name = "信内容"
        verbose_name_plural = verbose_name
        db_table = "message_text"


class Messages(BaseModel):
    sendID = models.ForeignKey(verbose_name="发送者", to=Users, on_delete=models.CASCADE, related_name="sender")
    recID = models.ForeignKey(verbose_name="接收者", to=Users, on_delete=models.CASCADE, null=True, blank=True,
                              related_name="receiver")
    text = models.ForeignKey(verbose_name="站内信消息", to=MessageText, on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name="阅读状态", null=True, blank=True)

    def __str__(self):
        return "({}) from {} to {}".format(self.id, self.sendID, self.recID)

    class Meta:
        verbose_name = "站内信"
        verbose_name_plural = verbose_name
        db_table = "messages"

    info_html = "<div>{}</div>"

    def text_id(self):
        return format_html(self.info_html, self.text.id)

    text_id.short_description = "内容id"

    def text_title(self):
        return format_html(self.info_html, self.text.title)

    text_title.short_description = "内容标题"

    def text_content(self):
        return format_html(self.info_html, self.text.content)

    text_content.short_description = "内容正文"

    def text_add_time(self):
        return format_html(self.info_html, self.text.add_time)

    text_add_time.short_description = "内容创建时间"

    def text_update_time(self):
        return format_html(self.info_html, self.text.add_time)

    text_update_time.short_description = "内容更新时间"


class MessageSysStatus(BaseModel):
    message = models.ForeignKey(verbose_name="消息", to=Messages, on_delete=models.CASCADE)
    recID = models.ForeignKey(verbose_name="用户", to=Users, on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name="阅读状态", default=False)

    def __str__(self):
        return "{}({}):{}".format(self.message, self.recID, self.status)

    class Meta:
        verbose_name = "系统通知阅读状态"
        verbose_name_plural = verbose_name
        db_table = "message_sys_status"

    info_html = "<div>{}</div>"

    def message_id(self):
        return format_html(self.info_html, self.message.id)

    message_id.short_description = "消息id"

    def text_title(self):
        return format_html(self.info_html, self.message.text.title)

    text_title.short_description = "消息标题"

    def text_content(self):
        return format_html(self.info_html, self.message.text.content)

    text_content.short_description = "消息正文"

    def message_add_time(self):
        return format_html(self.info_html, self.message.add_time)

    message_add_time.short_description = "消息创建时间"

    def message_update_time(self):
        return format_html(self.info_html, self.message.add_time)

    message_update_time.short_description = "消息更新时间"


def getNewSysMessageNum(user: Users) -> int:
    hotel: Users = None
    try:
        hotel = Users.objects.get(username="hotel")
    except Exception as e:
        raise Exception("Get Admin User Failed")
    num_sys = 0
    msg_list = Messages.objects.filter(Q(sendID=None) | Q(sendID=hotel)).filter(Q(recID=None) | Q(recID=user))
    for msg in msg_list:
        msg_list2 = MessageSysStatus.objects.filter(message=msg).filter(recID=user)
        if len(msg_list2) == 0:
            num_sys += 1
        else:
            for msg2 in msg_list2:
                if msg2.status is False:
                    num_sys += 1
    return num_sys


def getSysMessage(user: Users, if_new: int = 0, id: int = -1) -> dict:
    hotel: Users = None
    try:
        hotel = Users.objects.get(username="hotel")
    except Exception as e:
        raise Exception("Get Admin User Failed")
    num_sys = 0
    msg_list = Messages.objects.filter(Q(sendID=None) | Q(sendID=hotel)).filter(Q(recID=None) | Q(recID=user))
    data_list = []
    for msg in msg_list:
        new_flag = True
        msg_dict = {"msg_id": msg.id, "title": msg.text.title, "content": msg.text.content,
                    "add_time": msg.add_time.timestamp(), "status": False}
        msg_list2 = MessageSysStatus.objects.filter(message=msg).filter(recID=user)
        if len(msg_list2) != 0:
            for msg2 in msg_list2:
                if msg2.status is True:
                    new_flag = False
                    msg_dict["status"] = True
                    break
        if if_new == 0:  # 新消息
            if new_flag is False:
                continue
        elif if_new == 1:  # 旧消息
            if new_flag is True:
                continue
        elif if_new == 2:
            pass
        data_list.append(msg_dict)
    json_dict = {"id": id, "status": 0, "message": "Successful", "data": {"num": len(data_list), "list": data_list}}
    return json_dict


def getNewPrivateNum(user: Users) -> dict:
    hotel: Users = None
    try:
        hotel = Users.objects.get(username="hotel")
    except Exception as e:
        raise Exception("Get Admin User Failed")
    condition = ~Q(sendID=None) & ~Q(sendID=hotel) & Q(recID=user)
    msg_list = Messages.objects.filter(condition).filter(status=False).order_by("add_time")
    records_dict = {}
    num = 0
    for msg in msg_list:
        people = msg.sendID.username
        if people not in records_dict.keys():
            records_dict[people] = 0
        records_dict[people] += 1
        num += 1
    json_dict = records_dict

    return {"total": num, "detail": json_dict}


def getPrivateMessage(user: Users, if_new: int = 0, id: int = -1) -> dict:
    hotel: Users = None
    try:
        hotel = Users.objects.get(username="hotel")
    except Exception as e:
        raise Exception("Get Admin User Failed")
    condition = (~Q(sendID=None) & ~Q(sendID=hotel) & Q(recID=user)) | (
            Q(sendID=user) & ~Q(recID=hotel) & ~Q(recID=None))
    msg_list = Messages.objects.filter(condition).order_by("add_time")
    """
    data:{"units":[{"people":"123456789","records":[{"source":0,"title":"","content":"你好","add_time":"2020-2-1"}]},{},{}]}
    """
    records_dict = {}
    total_num = 0
    for msg in msg_list:
        if msg.sendID == user:
            people = msg.recID.username
            source = 1  # 用户发送的
        else:
            people = msg.sendID.username
            source = 0  # 用户接收的
        # 消息类型判断=====
        if if_new == 0:  # 新消息
            if msg.status is True or source == 1:
                continue
        elif if_new == 1:  # 旧消息
            if msg.status is False and source == 0:
                continue
        elif if_new == 2:
            pass
        # 判断结束=======
        if people not in records_dict.keys():
            records_dict[people] = []
        msg_dict = {"source": source, "msg_id": msg.id, "title": msg.text.title, "content": msg.text.content,
                    "add_time": msg.add_time.timestamp(), "status": msg.status}
        records_dict[people].append(msg_dict)
        total_num += 1
    units_list = []
    for people in records_dict.keys():
        units_dict = {"people": people, "num": len(records_dict[people]), "records": records_dict[people]}
        units_list.append(units_dict)
    json_dict = {"id": id, "status": 0, "message": "Successful",
                 "data": {"records_num": total_num, "unit_num": len(units_list), "list": units_list}}
    return json_dict
