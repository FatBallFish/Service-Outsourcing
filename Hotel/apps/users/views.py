from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from Hotel import settings

import json, base64
import os


# Create your views here.

# COS.Initialize(settings.BASE_DIR)
# Arcface.Initialize(False)
class UserLoginView(View):
