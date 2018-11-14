######################################
# Django 模块
######################################
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.views import View
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse

######################################
# 第三方模块
######################################
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

######################################
# 系统模块
######################################
import json
import datetime

######################################
# 自建模块
######################################
from utils.login_check import LoginStatusCheck
from .forms import *
from .models import *


######################################
# 添加平台用户列表
######################################
class EditPlatformUserView(LoginStatusCheck, View):
    def post(self, request):
        try:
            pu_id = request.POST.get('pu_id', '')
            if pu_id != '':
                pu = PlatformUserInfo.objects.get(id=int(pu_id))
                pu.username = request.POST.get('username', '')
                pu.password = request.POST.get('password', '')
                pu.update_user = request.user
                pu.save()
            else:
                platform_id = int(request.POST.get('platform_id'))
                pu = PlatformUserInfo()
                pu.platform_id = platform_id
                pu.username = request.POST.get('username', '')
                pu.password = request.POST.get('password', '')
                pu.user = request.user
                pu.update_user = request.user
                pu.save()

            return HttpResponse('{"status":"success", "msg":"修改用户成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"failed", "msg":"修改用户失败！"}', content_type='application/json')













