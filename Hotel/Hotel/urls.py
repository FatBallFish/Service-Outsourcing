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
from apps.faces.views import FaceView, FaceGroupView, FaceMaskView
from apps.users.views import UserLoginView, UserRegisterView, UserInfoView, CaptchaView, PasswordView, PortraitView, \
    UserSearchView
from apps.realauth.views import RealAuthView, DistrictView
from apps.devices.views import DeviceLoginView, DeviceRegisterView, DeviceHotelListView, DeviceFaceFeatureView, \
    DeviceListView, DeviceLockerView,DevicePassengerFlowView
from apps.msg.views import MsgView
from apps.pics.views import PicView
from apps.locker.views import LockerApplyView, LockerInfoView
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
    path(API_ROOT + "user/search/", csrf_exempt(UserSearchView.as_view()), name="user_search"),
    path(API_ROOT + "captcha/", csrf_exempt(CaptchaView.as_view()), name="captcha"),
    path(API_ROOT + "face/group/", csrf_exempt(FaceGroupView.as_view()), name="face_group"),
    path(API_ROOT + "face/", csrf_exempt(FaceView.as_view()), name="face_register"),
    path(API_ROOT + "face/mask/", csrf_exempt(FaceMaskView.as_view()), name="face_mask"),
    path(API_ROOT + "realauth/", csrf_exempt(RealAuthView.as_view()), name="real_auth"),
    path(API_ROOT + "map/district/", csrf_exempt(DistrictView.as_view()), name="district"),
    path(API_ROOT + "device/list/", csrf_exempt(DeviceListView.as_view()), name="device_list"),
    path(API_ROOT + "device/login/", csrf_exempt(DeviceLoginView.as_view()), name="device_login"),
    path(API_ROOT + "device/register/", csrf_exempt(DeviceRegisterView.as_view()), name="device_register"),
    path(API_ROOT + "device/hotel/", csrf_exempt(DeviceHotelListView.as_view()), name="device_hotel_list"),
    path(API_ROOT + "device/feature/", csrf_exempt(DeviceFaceFeatureView.as_view()), name="device_feature"),
    path(API_ROOT + "device/locker/", csrf_exempt(DeviceLockerView.as_view()), name="device_locker"),
    path(API_ROOT + "device/flow/", csrf_exempt(DevicePassengerFlowView.as_view()), name="device_flow"),
    path(API_ROOT + "pic/", csrf_exempt(PicView.as_view()), name="pic"),
    path(API_ROOT + "pic/get/<path:upload_to>/", csrf_exempt(PicView.as_view()), name="get_pic"),
    path(API_ROOT + "msg/", csrf_exempt(MsgView.as_view()), name="msg"),
    path(API_ROOT + "locker/apply/", csrf_exempt(LockerApplyView.as_view()), name="locker_apply"),
    path(API_ROOT + "locker/info/", csrf_exempt(LockerInfoView.as_view()), name="locker_info"),

]
