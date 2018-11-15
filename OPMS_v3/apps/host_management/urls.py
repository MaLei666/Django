"""
Host management app
"""
from django.urls import path
from host_management.views import *


app_name = 'host_management'

urlpatterns = [
    # 主机列表
    path('list', HostListView.as_view(), name='host_list'),

    # webssh
    path(r'webssh/<int:host_id>', WebSSHView.as_view(), name='web_ssh'),

    # 主机详情
    path('info/<int:host_id>', HostInfoView.as_view(), name='host_info'),

    # 添加主机
    path('info/add', AddHostInfoView.as_view(), name='add_host'),

    # 删除主机
    path('info/delete', DeleteHostView.as_view(), name='del_host'),
    # path('info/<int:host_id>', DeleteHostView.as_view(), name='del_host'),

    # 修改主机
    path('info/edit', EditHostInfoView.as_view(), name='edit_host'),
    # path('info/<int:host_id>', EditHostInfoView.as_view(), name='edit_host'),

    # 添加主机服务
    path('service/add', AddHostServiceView.as_view(), name='add_host_service'),

    # 修改主机服务
    path('service/edit', EditHostServiceView.as_view(), name='edit_host_service'),

    # 删除主机服务
    path('service/delete', DeleteHostServiceView.as_view(), name='del_host_service'),

    # 数据库列表
    path('database/list', DatabaseListView.as_view(), name='db_list'),

    # 数据库详情
    path('database/info/<int:db_id>', DatabaseInfoView.as_view(), name='db_info'),

    # 添加数据库信息
    path('database/add', AddDatabaseInfoView.as_view(), name='add_db'),

    # 修改数据库信息
    path('database/edit', EditDatabaseInfoView.as_view(), name='edit_db'),

    # 删除数据库信息
    path('database/delete', DeleteDatabaseInfoView.as_view(), name='del_db'),

    # 添加数据库库表
    path('database/db/add', AddDatabaseDBView.as_view(), name='add_db_db'),

    # 修改数据库库表
    path('database/db/edit', EditDatabaseDBView.as_view(), name='edit_db_db'),

    # 删除数据库库表
    path('database/db/delete', DeleteDatabaseDBView.as_view(), name='del_db_db'),

    # 添加数据库用户
    path('database/user/add', AddDatabaseUserView.as_view(), name='add_db_user'),

    # 修改数据库用户
    path('database/user/edit', EditDatabaseUserView.as_view(), name='edit_db_user'),

    # 删除数据库用户
    path('database/user/delete', DeleteDatabaseUserView.as_view(), name='del_db_user'),

    # 操作记录
    path('operation/record', HostOperationView.as_view(), name='host_op_record'),

]


