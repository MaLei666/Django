"""
User app
"""
from django.urls import path
from .views import *


app_name = 'spider_data'

urlpatterns = [
    # 首页
    path('', EditPlatformUserView.as_view(), name='data'),

]


