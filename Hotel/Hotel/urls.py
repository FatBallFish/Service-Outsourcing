"""Hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve
from django.views.decorators.csrf import csrf_exempt

from Hotel import settings
from apps.tokens.views import TokenDokiView, PingView
from apps.faces.views import FaceView, FaceGroupView
from apps.users.views import UserLoginView, UserRegisterView, UserInfoView, CaptchaView, PasswordView, PortraitView
from apps.realauth.views import RealAuthView
from apps.devices.views import DeviceLoginView, DeviceRegisterView, DeviceHotelListView
import os

API_ROOT = settings.API_ROOT
urlpatterns = [
    # 全局配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    path(API_ROOT + "ping/", PingView.as_view(), name="ping"),
    path(API_ROOT + "user/login/", csrf_exempt(UserLoginView.as_view()), name="user_login"),
    path(API_ROOT + "user/register/", csrf_exempt(UserRegisterView.as_view()), name="user_register"),
    path(API_ROOT + "user/doki/", csrf_exempt(TokenDokiView.as_view()), name="user_doki"),
    path(API_ROOT + "user/info/", csrf_exempt(UserInfoView.as_view()), name="user_info"),
    path(API_ROOT + "user/password/", csrf_exempt(PasswordView.as_view()), name="user_password"),
    path(API_ROOT + "user/portrait/", csrf_exempt(PortraitView.as_view()), name="user_portrait"),
    path(API_ROOT + "captcha/", csrf_exempt(CaptchaView.as_view()), name="captcha"),
    path(API_ROOT + "face/group/", csrf_exempt(FaceGroupView.as_view()), name="face_group"),
    path(API_ROOT + "face/", csrf_exempt(FaceView.as_view()), name="face_register"),
    path(API_ROOT + "realauth/", csrf_exempt(RealAuthView.as_view()), name="real_auth"),
    path(API_ROOT + "device/login/", csrf_exempt(DeviceLoginView.as_view()), name="device_login"),
    path(API_ROOT + "device/register/", csrf_exempt(DeviceRegisterView.as_view()), name="device_register"),
    path(API_ROOT + "device/hotel/", csrf_exempt(DeviceHotelListView.as_view()), name="device_hotel_list"),
]
