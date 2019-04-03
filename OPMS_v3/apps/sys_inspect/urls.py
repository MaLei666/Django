"""
Host management app
"""
from django.urls import path
from .views import *


app_name = 'sys_inspect'

urlpatterns = [
    # 设备列表
    path('device/list', InspectDevInfoViews.as_view(), name='inspect_devices_list'),

    # 添加设备
    path('device/add', AddDevView.as_view(), name='inspect_devices_add'),
    #
    # # # 运维平台列表
    # # path('ops/list', OpsPlatformListView.as_view(), name='platform_ops_list'),
    #
    # # 第三方平台列表
    # path('other/list', OtherPlatformListView.as_view(), name='platform_other_list'),
    #
    # # 添加第三方平台
    # path('other/add', AddOtherPlatformView.as_view(), name='platform_other_add'),
    #
    # # 修改平台用户列表
    # path('user/edit', EditPlatformUserView.as_view(), name='platform_user_edit'),
    #
    # 删除设备
    path('device/delete', DeleteDevView.as_view(), name='inspect_device_delete'),

    # 编辑设备
    path('device/edit', EditDevInfoView.as_view(), name='inspect_device_edit'),

]


