######################################
# Django 模块
######################################
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.views import View
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse

######################################
# 系统模块
######################################
import json
import datetime
from .forms import *
from .models import *
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage


######################################
# 主机列表
######################################
class DataView(View):
    def get(self, request):
        # 页面选择
        web_chose_left_1 = 'spider_data'
        web_chose_left_2 = 'data'
        web_chose_middle = ''

        # 获取主机记录
        data_records = DataInfo.objects.order_by('-update_time')

        # 关键字
        # keyword = request.GET.get('keyword', '')

        # if keyword != '':
        #     host_records = data_records.filter(Q(hot__icontains=keyword) | Q(
        #         use__name__icontains=keyword) | Q(project__name__icontains=keyword) | Q(desc__icontains=keyword))

        # 记录数量
        record_nums = data_records.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(data_records, 16, request=request)

        # 分页处理后的 QuerySet
        data_records = p.page(page)

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            # 'users': users,
            # 'keyword': keyword,
            'data_records': data_records,
            'record_nums': record_nums,
            # 'WEBSSH_IP': WEBSSH_IP,
            # 'WEBSSH_PORT': WEBSSH_PORT,
        }
        return render(request, 'spider_data/db_data.html', context=context)












