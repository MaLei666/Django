"""
User app
"""
from django.urls import path
from .views import *


app_name = 'spider_data'

urlpatterns = [
    # 问题列表页
    path('', DataView.as_view(), name='list'),
    path('info/<int:question_id>', InfoView.as_view(), name='info'),
    # path('info', InfoView.as_view(), name='info'),

]


