from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse
from django.db.models import Q

from apps.tokens.models import Doki2
from apps.devices.models import Device, DeviceDoki, DeviceGroup
from apps.passengerFlow.models import PassengerFlow, PassengerFace
from apps.rooms.models import Hotel

from datetime import datetime, timedelta
import json


# Create your views here.
class PassengerFlowView(View):
    def post(self, request, *args, **kwargs):
        try:
            token = request.GET.get("token")
            print("token:", token)
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        result, user = Doki2(token=token)
        if result is False:
            return JsonResponse({"id": -1, "status": -101, "message": "Error Token", "data": {}})
        try:
            data = dict(json.loads(request.body))
            print(data)
        except:
            json_dict = {"id": -1, "status": -1, "message": "Error JSON key", "data": {}}
            return JsonResponse(json_dict)
        if "id" in data.keys():
            id = data["id"]
        else:
            id = -1
            # 判断指定所需字段是否存在，若不存在返回status -1 json。
        for key in ["type", "subtype", "data"]:
            if key not in data.keys():
                # status -1 json的key错误。
                json_dict = {"id": id, "status": -1, "message": "Error JSON key", "data": {}}
                return JsonResponse(json_dict)
        type = data["type"]
        subtype = data["subtype"]
        data = dict(data["data"])
        if type == "flow":
            if subtype == "time":
                for key in ["hotel_id", "model"]:
                    if key not in data.keys():
                        # status -3 json的value错误。
                        return JsonResponse({"id": id, "status": -3, "message": "Error data key", "data": {}})
                hotel_id = data["hotel_id"]
                try:
                    hotel = Hotel.objects.get(id=hotel_id)
                except Exception as e:
                    # status 100 错误的酒店id
                    return JsonResponse({"id": id, "status": 100, "message": "Error hotel_id", "data": {}})
                model = data["model"]
                condition = Q(hotel=hotel)
                now = datetime.now()
                if model == "year":
                    this_year = datetime(now.year, 1, 1)
                    next_year = datetime(now.year + 1, 1, 1)
                    condition = condition & (Q(enter_time__gte=this_year) & Q(enter_time__lte=next_year))
                elif model == "month":
                    this_month = datetime(now.year, now.month, 1)
                    next_month = datetime(now.year, now.month + 1, 1)
                    condition = condition & (Q(enter_time__gte=this_month) & Q(enter_time__lte=next_month))
                elif model == "day":
                    this_day = datetime(now.year, now.month, now.day)
                    next_day = datetime(now.year, now.month, now.day + 1)
                    condition = condition & (Q(enter_time__gte=this_day) & Q(enter_time__lte=next_day))
                elif model == "":
                    pass
                flow_list = PassengerFlow.objects.filter(condition)
                for flow in flow_list:
                    pass


class NewOldTableView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = dict(json.loads(request.body))
            print(data)
        except:
            json_dict = {"id": -1, "status": -1, "message": "Error JSON key", "data": {}}
            return JsonResponse(json_dict)
        now = datetime.now()
        count_dict = {"new": 0, "old": 0}
        flow_list = PassengerFlow.objects.filter(enter_time__lte=now)
        for flow in flow_list:
            face = flow.face
            if face.name != "stranger":
                count_dict["old"] += 1
            else:
                count_dict["new"] += 1
        option2 = {
            "title": {
                "text": '常新客比例',
                "subtext": '数据截止{}'.format(now),
                "left": 'center'
            },
            "tooltip": {
                "trigger": 'item',
                "formatter": '{a} <br/>{b} : {c} ({d}%)'
            },
            "legend": {
                "orient": 'vertical',
                "left": 'left',
                "data": ['常客', '新客']
            },
            "series": [
                {
                    "name": '常新客比例',
                    "type": 'pie',
                    "radius": '55%',
                    "center": ['50%', '60%'],
                    "data": [
                        {"value": count_dict["old"], "name": '常客'},
                        {"value": count_dict["new"], "name": '新客'},
                    ],
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        }
        return JsonResponse(option2)


class WeekTableView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = dict(json.loads(request.body))
            print(data)
        except:
            json_dict = {"id": -1, "status": -1, "message": "Error JSON key", "data": {}}
            return JsonResponse(json_dict)
        now = datetime.now()
        weekday = now.weekday() + 1
        while weekday != 1:
            # 求出这周的周一那天
            now = now - timedelta(days=1)
            weekday = now.weekday() + 1
        time_line_data = []
        time_line_data_label = []
        options = []
        for i in range(7):
            # 获取每天数据
            time_line_data.append(now.strftime("%Y-%m-%d"))
            time_line_data_label.append(now.strftime("%m.%d"))
            condition = Q(enter_time__year=now.year) & Q(enter_time__month=now.month) & Q(enter_time__day=now.day)
            flow_list = PassengerFlow.objects.filter(condition)
            # 初始化计数字典
            count_dict = {}
            for j in range(24):
                count_dict[j] = 0
            # 开始计数
            for flow in flow_list:
                enter_time = flow.enter_time
                hour = enter_time.hour
                if hour in count_dict.keys():
                    count_dict[hour] += 1
                else:
                    count_dict[hour] = 1
            data_list = [count_dict[x] for x in count_dict.keys()]
            weekstr = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}
            option_dict = {
                "title": {"text": "{}月{}日星期{} 客流量".format(now.month, now.day, weekstr[now.weekday()])},
                "series": [{"name": "总人数", "data": data_list}, {"name": "折线总人数", "data": data_list}]
            }
            options.append(option_dict)
            now = now + timedelta(days=1)
        option = {
            "baseOption": {
                "timeline": {
                    "axisType": 'category',
                    "autoPlay": True,
                    "playInterval": 1000,
                    "data": time_line_data,
                },
                "title": {
                    "subtext": '数据来自客流统计'
                },
                "tooltip": {
                },
                "legend": {
                    "left": 'right',
                    "data": ['总人数', '折线总人数'],
                    "selected": {
                        '总人数': True,
                        '折线总人数': True,
                    }
                },
                "calculable": True,
                "grid": {
                    "top": 80,
                    "bottom": 100,
                    "tooltip": {
                        "trigger": 'axis',
                        "axisPointer": {
                            "type": 'shadow',
                            "label": {
                                "show": True,
                            }
                        }
                    }
                },
                "xAxis": [
                    {
                        'type': 'category',
                        'axisLabel': {'interval': 0},
                        'data': [
                            '0时', '\n1时', '2时', '\n3时', '4时', '\n5时', '6时', '\n7时',
                            '8时', '\n9时', '10时', '\n11时', '12时', '\n13时', '14时', '\n15时',
                            '16时', '\n17时', '18时', '\n19时', '20时', '\n21时', '22时', '\n23时',
                        ],
                        "splitLine": {"show": False}
                    }
                ],
                "yAxis": [
                    {
                        "type": 'value',
                        "name": '人数（次）'
                    }
                ],
                "series": [
                    {"name": '总人数', "type": 'bar'},
                    {"name": '折线总人数', "type": "line"},
                ]
            },
            "options": options,
        }
        # print(option)
        return JsonResponse(option)


class DayTableView(View):
    """
    还没做好，暂时放着
    """

    def post(self, request, *args, **kwargs):
        option = {
            "title": {
                "text": '{} 实时客流数据'
            },
            "tooltip": {
                "trigger": 'axis'
            },
            "legend": {
                "data": ['总人数', '联盟广告', '视频广告', '直接访问', '搜索引擎']
            },
            "grid": {
                "left": '3%',
                "right": '4%',
                "bottom": '3%',
                "containLabel": True
            },
            "toolbox": {
                "feature": {
                    "saveAsImage": {}
                }
            },
            "xAxis": {
                "type": 'category',
                "boundaryGap": False,
                "data": ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            },
            "yAxis": {
                "type": 'value'
            },
            "series": [
                {
                    "name": '邮件营销',
                    "type": 'line',
                    "stack": '总量',
                    "data": [120, 132, 101, 134, 90, 230, 210]
                },
                {
                    "name": '联盟广告',
                    "type": 'line',
                    "stack": '总量',
                    "data": [220, 182, 191, 234, 290, 330, 310]
                },
                {
                    "name": '视频广告',
                    "type": 'line',
                    "stack": '总量',
                    "data": [150, 232, 201, 154, 190, 330, 410]
                },
                {
                    "name": '直接访问',
                    "type": 'line',
                    "stack": '总量',
                    "data": [320, 332, 301, 334, 390, 330, 320]
                },
                {
                    "name": '搜索引擎',
                    "type": 'line',
                    "stack": '总量',
                    "data": [820, 932, 901, 934, 1290, 1330, 1320]
                }
            ]
        }


class AgeTableView(View):
    def post(self, request, *args, **kwargs):
        now = datetime.now()
        data_list = []
        count_dict = {}
        for i in range(10):
            count_dict[i] = 0
        count_dict[-1] = 0
        # condition = Q(enter_time__year=now.year) & Q(enter_time__month=now.month) & Q(enter_time__day=now.day)
        flow_list = PassengerFlow.objects.filter(enter_time__lte=now)
        for flow in flow_list:
            face = flow.face
            age = face.age
            if age is None or age < 0:
                count_dict[-1] += 1
                continue
            index = age // 10
            if index > 9:
                count_dict[9] += 1
                continue
            count_dict[index] += 1
        for key in count_dict.keys():
            if key == -1:
                # 特殊情况，年龄未知
                option_dict = {"value": count_dict[-1], "name": "未知"}
            elif key == 9:
                # 特殊情况，年龄90岁即以上
                option_dict = {"value": count_dict[9], "name": "90岁及以上"}
            else:
                option_dict = {"value": count_dict[key], "name": "{}-{}岁".format(key * 10, key * 10 + 9)}
            data_list.append(option_dict)

        option = {
            "title": {
                "text": '客流年龄段统计',
                "subtext": '数据截止{}'.format(now),
                "left": 'center'
            },
            "tooltip": {
                "trigger": 'item',
                "formatter": '{a} <br/>{b}: {c} ({d}%)'
            },
            "legend": {
                "orient": 'vertical',
                "left": 10,
                "data": ['0-9岁', '10-19岁', '20-29岁', '30-39岁', '40-49岁', "50-59岁", "60-69岁", "70-79岁", "80-89岁",
                         "90岁及以上", "未知"]
            },
            "series": [
                {
                    "name": '客流年龄段',
                    "type": 'pie',
                    "radius": ['50%', '70%'],
                    "avoidLabelOverlap": False,
                    "label": {
                        "show": False,
                        "position": 'center'
                    },
                    "emphasis": {
                        "label": {
                            "show": True,
                            "fontSize": '30',
                            "fontWeight": 'bold'
                        }
                    },
                    "labelLine": {
                        "show": False
                    },
                    "data": data_list
                }
            ]
        }
        print(option)
        return JsonResponse(option)


class FlowSumCardView(View):
    def post(self, request, *args, **kwargs):
        num = len(PassengerFlow.objects.all())
        return JsonResponse({"num": num})


class SumFlowTableView(View):
    def post(self, request, *args, **kwargs):
        num = len(PassengerFlow.objects.all())
        option = {
            "tooltip": {
                "formatter": '{a} <br/>{b} : {c}%'
            },
            "toolbox": {
                "feature": {
                    "restore": {},
                    "saveAsImage": {}
                }
            },
            "series": [
                {
                    "name": '累计客流量',
                    "type": 'gauge',
                    "detail": {"formatter": '{value}人'},
                    "data": [{"value": num, "name": '累计客流量'}]
                }
            ]
        }
        return JsonResponse(option)
