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
from operation_record.models import UserOperationRecord
from opms.settings import WEBSSH_IP, WEBSSH_PORT


##############################################################################
# 主机资产模块
##############################################################################

######################################
# 主机列表
######################################
class HostListView(LoginStatusCheck, View):
    def get(self, request):
        if request.user.role > 1:
            # 页面选择
            web_chose_left_1 = 'host_management'
            web_chose_left_2 = 'host'
            web_chose_middle = ''

            # 用户
            users = UserProfile.objects.filter(status=1)

            # 获取主机记录
            host_records = HostInfo.objects.filter(status=1).order_by('-update_time')

            # 关键字
            keyword = request.GET.get('keyword', '')
            if keyword != '':
                host_records = host_records.filter(Q(hostname__icontains=keyword) | Q(
                    use__name__icontains=keyword) | Q(project__name__icontains=keyword) | Q(desc__icontains=keyword))

            # 记录数量
            record_nums = host_records.count()

            # 判断页码
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            # 对取到的数据进行分页，记得定义每页的数量
            p = Paginator(host_records, 16, request=request)

            # 分页处理后的 QuerySet
            host_records = p.page(page)

            context = {
                'web_chose_left_1': web_chose_left_1,
                'web_chose_left_2': web_chose_left_2,
                'web_chose_middle': web_chose_middle,
                'users': users,
                'keyword': keyword,
                'host_records': host_records,
                'record_nums': record_nums,
                'WEBSSH_IP': WEBSSH_IP,
                'WEBSSH_PORT': WEBSSH_PORT,
            }
            return render(request, 'host_management/host/host_list.html', context=context)
        else:
            return HttpResponse(status=403)


########################################################################################################################
## wessh主机视图
########################################################################################################################
class WebSSHView(LoginStatusCheck, View):
    def post(self, request, host_id):
        host = HostInfo.objects.get(id=int(host_id))
        ret = {}
        try:
            if host.out_ip:
                ip = host.out_ip
            else:
                ip = host.in_ip

            port = host.ssh_port

            if host.normal_user:
                username = host.normal_user
                password = host.normal_pass
            else:
                username = host.admin_user
                password = host.admin_pass

            ret = {"ip": ip, 'port': port, "username": username, 'password': password, "static": True}
        except Exception as e:
            ret['status'] = False
            ret['error'] = '请求错误,{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


######################################
# 添加主机
######################################
class AddHostInfoView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            add_host_info_form = AddHostInfoForm(request.POST)
            if add_host_info_form.is_valid():
                in_ip = request.POST.get('in_ip')

                if HostInfo.objects.filter(in_ip=in_ip).filter(status=1):
                    return HttpResponse('{"status":"failed", "msg":"该 IP 的主机已经存在，请检查！"}',
                                        content_type='application/json')

                host = HostInfo()
                host.in_ip = request.POST.get('in_ip')
                host.out_ip = request.POST.get('out_ip', '')
                # host.system_id = int(request.POST.get('system'))
                host.hostname = request.POST.get('hostname')
                host.ssh_port = int(request.POST.get('ssh_port'))
                host.root_ssh = request.POST.get('root_ssh')
                host.admin_user = request.POST.get('admin_user')
                host.admin_pass = request.POST.get('admin_pass')
                host.update_user = request.user
                host.desc = request.POST.get('desc', '')
                host.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = host.id
                op_record.operation = 1
                # op_record.action = "添加 [ %s ] 机房主机：%s" % (host.idc.name, host.in_ip)
                op_record.save()
                return HttpResponse('{"status":"success", "msg":"主机信息添加成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"主机信息填写错误，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 主机详情
######################################
class HostInfoView(LoginStatusCheck, View):
    def get(self, request, host_id):
        # 页面选择
        web_chose_left_1 = 'host_management'
        web_chose_left_2 = 'host'
        web_chose_middle = ''

        # 用户
        users = UserProfile.objects.filter(status=1)

        # 信息
        records = HostInfo.objects.get(id=host_id)

        # 服务
        services = HostServiceInfo.objects.filter(host_id=host_id).filter(status=1)

        # 判断是否添加数据库
        is_install_db = DatabaseInfo.objects.filter(host_id=int(host_id)).filter(status=1)

        if is_install_db:
            for each in is_install_db:
                have_db_id = each.id
        else:
            have_db_id = ''

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'records': records,
            'users': users,
            'services': services,
            'have_db_id': have_db_id,
        }
        return render(request, 'host_management/host/host_info.html', context=context)


######################################
# 删除主机
######################################
class DeleteHostView(LoginStatusCheck, View):
    def post(self, request):
        try:
            host_id = request.POST.get('host_id')
            host = HostInfo.objects.get(id=int(host_id))
            host.update_user = request.user
            host.status = 0
            host.save()

            # 添加操作记录
            op_record = UserOperationRecord()
            op_record.op_user = request.user
            op_record.belong = 1
            op_record.status = 1
            op_record.op_num = host.id
            op_record.operation = 4
            op_record.action = "停用 [ %s ] 机房主机：%s" % (host.idc.name, host.in_ip)
            op_record.save()

            return HttpResponse('{"status":"success", "msg":"主机删除成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"falied", "msg":"主机删除失败！"}', content_type='application/json')


######################################
# 修改主机
######################################
class EditHostInfoView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            edit_host_info_form = EditHostInfoForm(request.POST)
            if edit_host_info_form.is_valid():

                # 获取主机
                host_id = int(request.POST.get('host_id'))
                host = HostInfo.objects.get(id=host_id)
                host.in_ip = request.POST.get('in_ip')
                host.out_ip = request.POST.get('out_ip', '')
                host.hostname = request.POST.get('hostname')
                host.ssh_port = int(request.POST.get('ssh_port'))
                host.root_ssh = request.POST.get('root_ssh')
                host.admin_user = request.POST.get('admin_user')
                host.admin_pass = request.POST.get('admin_pass')
                host.op_user_id = int(request.POST.get('op_user'))
                host.update_user = request.user
                host.desc = request.POST.get('desc', '')
                host.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = host.id
                op_record.operation = 2
                op_record.action = "修改主机：%s" % host.in_ip
                op_record.save()

                return HttpResponse('{"status":"success", "msg":"主机信息修改成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"主机信息填写错误，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 数据库列表
######################################
class DatabaseListView(LoginStatusCheck, View):
    def get(self, request):
        # 页面选择
        web_chose_left_1 = 'host_management'
        web_chose_left_2 = 'database'
        web_chose_middle = ''

        # 主机列表
        hosts = HostInfo.objects.filter(status=1)
        # 用户
        users = UserProfile.objects.filter(status=1)
        # 数据库记录
        db_records = DatabaseInfo.objects.filter(status=1).order_by('-update_time')

        # 记录数量
        record_nums = db_records.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(db_records, 16, request=request)

        # 分页处理后的 QuerySet
        db_records = p.page(page)

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'hosts': hosts,
            'users': users,
            'record_nums': record_nums,
            'db_records': db_records,
        }
        return render(request, 'host_management/host/db_list.html', context=context)


######################################
# 数据库详情
######################################
class DatabaseInfoView(LoginStatusCheck, View):
    def get(self, request, db_id):
        # 页面选择
        web_chose_left_1 = 'host_management'
        web_chose_left_2 = 'database'
        web_chose_middle = ''
        # 用户
        users = UserProfile.objects.filter(status=1)
        # 主机列表
        hosts = HostInfo.objects.filter(status=1)

        # 数据库基本信息
        db_records = DatabaseInfo.objects.get(id=int(db_id))
        # 数据库库信息
        db_db_records = DatabaseDBInfo.objects.filter(db_id=int(db_id)).filter(status=1).order_by('-update_time')
        # 数据库用户信息
        db_user_records = DatabaseUserInfo.objects.filter(db_id=int(db_id)).filter(status=1).order_by('-update_time')

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'db_records': db_records,
            'db_db_records': db_db_records,
            'db_user_records': db_user_records,
            'users': users,
            'hosts': hosts,

        }
        return render(request, 'host_management/host/db_info.html', context=context)


######################################
# 添加数据库记录
######################################
class AddDatabaseInfoView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            if DatabaseInfo.objects.filter(host_id=int(request.POST.get('host_id'))).filter(status=1):
                return HttpResponse('{"status":"failed", "msg":"该主机的记录已经存在，请检查！"}', content_type='application/json')

            add_db_info_form = AddDatabaseInfoForm(request.POST)

            if add_db_info_form.is_valid():
                db_info = DatabaseInfo()
                db_info.host_id = int(request.POST.get('host_id'))
                db_info.db_name = request.POST.get('db_name')
                db_info.db_version = request.POST.get('db_version')
                db_info.db_admin_user = request.POST.get('db_admin_user')
                db_info.db_admin_pass = request.POST.get('db_admin_pass')
                db_info.desc = request.POST.get('desc', '')
                db_info.add_user = request.user
                db_info.update_user = request.user
                db_info.status = 1
                db_info.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = db_info.id
                op_record.operation = 1
                op_record.action = "添加数据库记录：%s" % (db_info.host.in_ip)
                op_record.save()

                return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"填写不合法，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 修改数据库记录
######################################
class EditDatabaseInfoView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            edit_db_info_form = EditDatabaseInfoForm(request.POST)
            if edit_db_info_form.is_valid():
                db_info = DatabaseInfo.objects.get(id=int(request.POST.get('db_id')))

                # 判断记录是否重复
                db_host = int(request.POST.get('host_id'))

                if db_info.host_id != db_host:
                    if DatabaseInfo.objects.filter(host_id=db_host).filter(status=1):
                        return HttpResponse('{"status":"failed", "msg":"该主机的记录已经存在，请检查！"}',
                                            content_type='application/json')

                # 不重复继续修改
                db_info.host_id = db_host
                db_info.db_name = request.POST.get('db_name')
                db_info.db_version = request.POST.get('db_version')
                db_info.db_admin_user = request.POST.get('db_admin_user')
                db_info.db_admin_pass = request.POST.get('db_admin_pass')
                db_info.desc = request.POST.get('desc', '')
                db_info.update_user = request.user
                db_info.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = db_info.id
                op_record.operation = 2
                op_record.action = "修改数据库记录：%s" % (db_info.host.in_ip)
                op_record.save()

                return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"填写不合法，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 删除数据库记录
######################################
class DeleteDatabaseInfoView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            db_info = DatabaseInfo.objects.get(id=int(request.POST.get('db_id')))
            db_info.status = 0
            db_info.update_user = request.user
            db_info.save()

            # 添加操作记录
            op_record = UserOperationRecord()
            op_record.op_user = request.user
            op_record.belong = 1
            op_record.status = 1
            op_record.op_num = db_info.id
            op_record.operation = 4
            op_record.action = "停用数据库记录：%s" % (db_info.host.in_ip)
            op_record.save()

            return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 添加数据库库表
######################################
class AddDatabaseDBView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            if DatabaseDBInfo.objects.filter(db_id=int(request.POST.get('db_id'))).filter(
                    name=request.POST.get('name')).filter(status=1):
                return HttpResponse('{"status":"failed", "msg":"该记录已经存在，请检查！"}', content_type='application/json')

            add_db_form = AddDatabaseDBForm(request.POST)

            if add_db_form.is_valid():
                db_info = DatabaseDBInfo()
                db_info.db_id = request.POST.get('db_id')
                db_info.name = request.POST.get('name')
                db_info.add_time=datetime.datetime.now()
                # db_info.use = request.POST.get('use')
                db_info.desc = request.POST.get('desc', '')
                db_info.add_user = request.user
                # db_info.update_user = request.user
                db_info.status = 1
                db_info.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = db_info.id
                op_record.operation = 1
                op_record.action = "添加主机 [ %s ] 的数据库：%s" % (db_info.db.host.in_ip, db_info.name)
                op_record.save()

                return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"填写不合法，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 编辑数据库库
######################################
class EditDatabaseDBView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            db_info = DatabaseDBInfo.objects.get(id=int(request.POST.get('db_id')))

            # 判断记录是否存在
            if db_info.name != request.POST.get('name'):
                if DatabaseDBInfo.objects.filter(db_id=int(request.POST.get('db_db_id'))).filter(
                        name=request.POST.get('name')).filter(status=1):
                    return HttpResponse('{"status":"failed", "msg":"该记录已经存在，请检查！"}', content_type='application/json')

            edit_db_form = EditDatabaseDBForm(request.POST)

            if edit_db_form.is_valid():
                db_info.db_id = int(request.POST.get('db_db_id'))
                db_info.name = request.POST.get('name')
                # db_info.use = request.POST.get('use')
                db_info.desc = request.POST.get('desc', '')
                db_info.update_user = request.user
                db_info.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = db_info.id
                op_record.operation = 2
                op_record.action = "修改主机 [ %s ] 的数据库：%s" % (db_info.db.host.in_ip, db_info.name)
                op_record.save()

                return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"填写不合法，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 删除数据库库
######################################
class DeleteDatabaseDBView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            db_info = DatabaseDBInfo.objects.get(id=int(request.POST.get('db_id')))
            db_info.update_user = request.user
            db_info.status = 0
            db_info.save()

            # 添加操作记录
            op_record = UserOperationRecord()
            op_record.op_user = request.user
            op_record.belong = 1
            op_record.status = 1
            op_record.operation = 4
            op_record.action = "删除主机 [ %s ] 的数据库：%s" % (db_info.db.host.in_ip, db_info.name)
            op_record.save()

            return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 添加数据库用户
######################################
class AddDatabaseUserView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            # 判断用户
            db_user = DatabaseUserInfo.objects.filter(db_id=int(request.POST.get('db_id'))).filter(
                username=request.POST.get('username'))
            if db_user:
                return HttpResponse('{"status":"failed", "msg":"该用户已存在，请检查！"}', content_type='application/json')

            add_db_user_form = AddDatabaseUserForm(request.POST)
            if add_db_user_form.is_valid():
                db_user = DatabaseUserInfo()
                db_user.db_id = int(request.POST.get('db_id'))
                db_user.username = request.POST.get('username')
                db_user.password = request.POST.get('password')
                db_user.grant_login = request.POST.get('grant_login')
                db_user.desc = request.POST.get('desc', '')
                db_user.add_user = request.user
                db_user.update_user = request.user
                db_user.status = 1
                db_user.save()

                for each in request.POST.getlist('dbs'):
                    db = DatabaseDBInfo.objects.get(id=int(each))
                    db_user.grant_db.add(db)
                    db_user.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = db_user.id
                op_record.operation = 1
                op_record.action = "添加主机 [ %s ] 的数据库用户：%s" % (db_user.db.host.in_ip, db_user.username)
                op_record.save()

                return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"填写不合法，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 编辑数据库用户
######################################
class EditDatabaseUserView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            # 判断用户
            db_user = DatabaseUserInfo.objects.get(id=int(request.POST.get('db_user_id')))

            new_username = request.POST.get('username')

            if db_user.username != new_username:
                if DatabaseUserInfo.objects.filter(username=new_username).filter(status=1):
                    return HttpResponse('{"status":"failed", "msg":"该用户已存在，请检查！"}', content_type='application/json')

            edit_db_user_form = EditDatabaseUserForm(request.POST)
            if edit_db_user_form.is_valid():
                db_user.username = request.POST.get('username')
                db_user.password = request.POST.get('password')
                db_user.grant_login = request.POST.get('grant_login')
                db_user.desc = request.POST.get('desc', '')
                db_user.update_user = request.user
                db_user.grant_db.clear()
                db_user.save()

                for each in request.POST.getlist('dbs'):
                    db = DatabaseDBInfo.objects.get(id=int(each))
                    db_user.grant_db.add(db)
                    db_user.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = db_user.id
                op_record.operation = 2
                op_record.action = "修改主机 [ %s ] 的数据库用户：%s" % (db_user.db.host.in_ip, db_user.username)
                op_record.save()

                return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"填写不合法，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 删除数据库用户
######################################
class DeleteDatabaseUserView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            # 判断用户
            db_user = DatabaseUserInfo.objects.get(id=int(request.POST.get('db_user_id')))
            db_user.status = 0
            db_user.update_user = request.user
            db_user.save()

            # 添加操作记录
            op_record = UserOperationRecord()
            op_record.op_user = request.user
            op_record.belong = 1
            op_record.status = 1
            op_record.op_num = db_user.id
            op_record.operation = 4
            op_record.action = "停用主机 [ %s ] 的数据库用户：%s" % (db_user.db.host.in_ip, db_user.username)
            op_record.save()

            return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


##############################################################################
# 基础配置模块
##############################################################################


######################################
# 添加系统服务
######################################
class AddHostServiceView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            add_service_form = AddHostServiceForm(request.POST)
            if add_service_form.is_valid():
                service = HostServiceInfo()
                host = int(request.POST.get('host_id'))
                service.host_id = host
                service.name = request.POST.get('name')
                service.version = request.POST.get('version')
                service.listen_user = request.POST.get('listen_user')
                service.listen_port = request.POST.get('listen_port')
                service.ins_path = request.POST.get('ins_path')
                service.log_path = request.POST.get('log_path')
                service.backup_path = request.POST.get('backup_path', '')
                service.start_cmd = request.POST.get('start_cmd')
                service.desc = request.POST.get('desc', '')
                service.add_user = request.user
                service.update_user = request.user
                service.status = 1
                service.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = service.id
                op_record.operation = 1
                op_record.action = "添加主机 [ %s ] 的服务：%s" % (service.host.in_ip, service.name)
                op_record.save()

                return HttpResponse('{"status":"success", "msg":"主机服务添加成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"主机服务填写不合法，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 编辑系统服务
######################################
class EditHostServiceView(LoginStatusCheck, View):
    def post(self, request):
        if request.user.role > 1:
            edit_service_form = EditHostServiceForm(request.POST)
            if edit_service_form.is_valid():
                service = HostServiceInfo.objects.get(id=int(request.POST.get('ser_id')))
                service.name = request.POST.get('name')
                service.version = request.POST.get('version')
                service.listen_user = request.POST.get('listen_user')
                service.listen_port = request.POST.get('listen_port')
                service.ins_path = request.POST.get('ins_path')
                service.log_path = request.POST.get('log_path')
                service.backup_path = request.POST.get('backup_path', '')
                service.start_cmd = request.POST.get('start_cmd')
                service.desc = request.POST.get('desc', '')
                service.update_user = request.user
                service.save()

                # 添加操作记录
                op_record = UserOperationRecord()
                op_record.op_user = request.user
                op_record.belong = 1
                op_record.status = 1
                op_record.op_num = service.id
                op_record.operation = 2
                op_record.action = "修改主机 [ %s ] 的服务：%s" % (service.host.in_ip, service.name)
                op_record.save()

                return HttpResponse('{"status":"success", "msg":"主机服务修改成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"failed", "msg":"主机服务填写不合法，请检查！"}', content_type='application/json')
        else:
            return HttpResponse(status=403)


######################################
# 删除服务
######################################
class DeleteHostServiceView(LoginStatusCheck, View):
    def post(self, request):
        try:
            ser_id = request.POST.get('ser_id')
            service = HostServiceInfo.objects.get(id=int(ser_id))
            service.update_user = request.user
            service.status = 0
            service.save()

            # 添加操作记录
            op_record = UserOperationRecord()
            op_record.op_user = request.user
            op_record.belong = 1
            op_record.status = 1
            op_record.op_num = service.id
            op_record.operation = 4
            op_record.action = "停用主机 [ %s ] 的服务：%s" % (service.host.in_ip, service.name)
            op_record.save()

            return HttpResponse('{"status":"success", "msg":"服务删除成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"falied", "msg":"服务删除失败！"}', content_type='application/json')

######################################
# 主机操作记录
######################################
class HostOperationView(LoginStatusCheck, View):
    def get(self, request):
        if request.user.role > 1:
            # 页面选择
            web_chose_left_1 = 'log_management'
            web_chose_left_2 = 'op_log'
            web_chose_middle = ''

            records = UserOperationRecord.objects.filter(belong=1).order_by('-add_time')

            # 关键字
            keyword = request.GET.get('keyword', '')
            if keyword != '':
                records = records.filter(
                    Q(op_user__chinese_name=keyword) | Q(action__icontains=keyword))

            # 用户选择
            user_check = request.GET.get('user_check', 'all')

            # 添加
            if user_check == 'add':
                records = records.filter(operation=1)

            # 修改
            if user_check == 'edit':
                records = records.filter(operation=2)

            # 启用
            if user_check == 'up':
                records = records.filter(operation=3)

            # 停用
            if user_check == 'down':
                records = records.filter(operation=4)

            # 数量
            record_nums = records.count()

            # 判断页码
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            # 对取到的数据进行分页，记得定义每页的数量
            p = Paginator(records, 19, request=request)

            # 分页处理后的 QuerySet
            records = p.page(page)

            context = {
                'web_chose_left_1': web_chose_left_1,
                'web_chose_left_2': web_chose_left_2,
                'web_chose_middle': web_chose_middle,
                'records': records,
                'keyword': keyword,
                'record_nums': record_nums,
                'user_check': user_check,
            }
            return render(request, 'host_management/other/host_op_record.html', context=context)
        else:
            return HttpResponse(status=403)









