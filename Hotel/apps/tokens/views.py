from django.shortcuts import render
from django.views import View
from django.http import JsonResponse,HttpResponse

from apps.tokens.models import Tokens

from datetime import datetime,timedelta
# Create your views here.
class TokenDokiView(View):
    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get("token")
            print("token:", token)
        except Exception as e:
            print(e)
            print("Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return JsonResponse({"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        Token_list = Tokens.objects.filter(token=token)
        if len(Token_list) != 1:
            return JsonResponse({"id": -1, "status": -101, "message": "Error token", "data": {}})
        Token = Token_list[0]
        Token.expire_time = datetime.now() + timedelta(minutes=10)
        Token.save()
        return JsonResponse({"id": -1, "status": 0, "message": "Successful", "data": {}})

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
        Token_list = Tokens.objects.filter(token=token)
        if len(Token_list) != 1:
            return {"id": -1, "status": -101, "message": "Error token", "data": {}}
        Token = Token_list[0]
        Token.expire_time = datetime.now() + timedelta(minutes=10)
        Token.save()
        if len(Token_list) != 1:
            return JsonResponse({"id": -1, "status": -101, "message": "Error token", "data": {}})
        Token = Token_list[0]
        Token.expire_time = datetime.now() + timedelta(minutes=10)
        Token.save()
        return JsonResponse({"id": -1, "status": 0, "message": "Successful", "data": {}})


class PingView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("pong")

    def post(self, request, *args, **kwargs):
        return JsonResponse({"id": -1, "status": 0, "message": "pong", "data": {}})
