"""
Host management app
"""
from django.urls import path
from .views import *


app_name = 'platform_management'

urlpatterns = [
    # 设备列表
    path('inspect/devices', InspectDevInfoViews.as_view(), name='inspect_devices_list'),

    # # 添加内部平台
    # path('company/add', AddCompanyPlatformView.as_view(), name='platform_company_add'),
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
    # # 删除平台
    # path('plat/delete', DeletePlatformView.as_view(), name='platform_delete'),
    #
    # # 编辑平台
    # path('plat/edit', EditPlatInfoView.as_view(), name='platform_edit'),

]


