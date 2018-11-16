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
# 问题列表
######################################
class DataView(View):
    def get(self, request):
        # 页面选择
        web_chose_left_1 = 'spider_data'
        web_chose_left_2 = 'list'
        web_chose_middle = ''

        # 获取问题记录
        data_records = DataList.objects.order_by('id')

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
        p = Paginator(data_records, 10, request=request)

        # 分页处理后的 QuerySet
        data_records = p.page(page)

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'data_records': data_records,
            'record_nums': record_nums,
        }
        return render(request, 'spider_data/data_list.html', context=context)


######################################
# 问题回答列表
######################################
class  InfoView(View):
    def get(self, request,question_id):
        # 页面选择
        web_chose_left_1 = 'spider_data'
        web_chose_left_2 = 'question'
        web_chose_middle = ''

        # 获取问题详情
        info_records = DataInfo.objects.get(id=question_id).order_by('-update_time')

        # 关键字
        # keyword = request.GET.get('keyword', '')

        # if keyword != '':
        #     host_records = data_records.filter(Q(hot__icontains=keyword) | Q(
        #         use__name__icontains=keyword) | Q(project__name__icontains=keyword) | Q(desc__icontains=keyword))

        # 记录数量
        record_nums = info_records.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(info_records,10, request=request)

        # 分页处理后的 QuerySet
        info_records = p.page(page)

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'info_records': info_records,
            'record_nums': record_nums,
        }
        return render(request, 'spider_data/data_info.html', context=context)









