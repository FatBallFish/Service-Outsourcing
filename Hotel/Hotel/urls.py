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
from apps.faces.views import FaceRegisterView
from apps.users.views import UserLoginView
import os

API_ROOT = "api/"
urlpatterns = [
    # 全局配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    path(API_ROOT + "face/register/", csrf_exempt(FaceRegisterView.as_view()), name="face_register"),
    path(API_ROOT + "user/login/", csrf_exempt(UserLoginView.as_view()), name="user_login"),
]
