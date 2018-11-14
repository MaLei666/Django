#####################################
# Django 模块
######################################
from django.db import models
from django.db.models import Q

######################################
# 系统模块
######################################
import datetime

######################################
# 自定义模块
######################################
from users.models import UserProfile

######################################
# 主机信息表
######################################
class HostInfo(models.Model):
    in_ip = models.GenericIPAddressField(verbose_name='内网IP')
    out_ip = models.GenericIPAddressField(verbose_name='外网IP', blank=True, null=True)
    hostname = models.CharField(verbose_name='主机名', max_length=30)
    ssh_port = models.IntegerField(verbose_name='远程端口',null=True)
    root_ssh = models.BooleanField(verbose_name='是否允许 root 远程', default=True)
    admin_user = models.CharField(verbose_name='管理员用户', max_length=20)
    admin_pass = models.CharField(verbose_name='管理员密码', max_length=50)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    update_user = models.ForeignKey(UserProfile, related_name='host_update_user', verbose_name='修改人',
                                    on_delete=models.CASCADE)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    desc = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((1, '正常'), (0, '停用')), default=1)

    class Meta:
        verbose_name = '主机信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.in_ip


######################################
# 服务信息表
######################################
class HostServiceInfo(models.Model):
    host = models.ForeignKey(HostInfo, verbose_name='主机', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='服务名称', max_length=30)
    version = models.CharField(verbose_name='服务版本', max_length=20, blank=True, null=True)
    listen_user = models.CharField(verbose_name='监听用户', max_length=20)
    listen_port = models.CharField(verbose_name='监听端口', max_length=30)
    ins_path = models.CharField(verbose_name='安装路径', max_length=100)
    log_path = models.CharField(verbose_name='日志路径', max_length=100, blank=True, null=True)
    backup_path = models.CharField(verbose_name='备份路径', max_length=100, blank=True, null=True)
    start_cmd = models.CharField(verbose_name='启动命令', max_length=100)
    desc = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)
    add_user = models.ForeignKey(UserProfile, related_name='se_add_user', verbose_name='添加人', on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    update_user = models.ForeignKey(UserProfile, related_name='se_update_user', verbose_name='修改人',
                                    on_delete=models.CASCADE)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((1, '正常'), (0, '停用')))

    class Meta:
        verbose_name = '主机服务信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


######################################
# 数据库表
######################################
class DatabaseInfo(models.Model):
    host = models.ForeignKey(HostInfo, verbose_name='主机', related_name='db_host', on_delete=models.CASCADE)
    db_name = models.CharField(verbose_name='数据库名称', max_length=20, blank=True, null=True)
    db_version = models.CharField(verbose_name='数据库版本', max_length=20, blank=True, null=True)
    db_admin_user = models.CharField(verbose_name='数据库管理员', max_length=20)
    db_admin_pass = models.CharField(verbose_name='数据库管理员密码', max_length=50)
    add_user = models.ForeignKey(UserProfile, related_name='db_add_user', verbose_name='添加人', on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    update_user = models.ForeignKey(UserProfile, related_name='db_update_user', verbose_name='修改人',
                                    on_delete=models.CASCADE)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    desc = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((1, '正常'), (0, '停用')), default=1)

    class Meta:
        verbose_name = '数据库信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.host.in_ip


######################################
# 数据库库表
######################################
class DatabaseDBInfo(models.Model):
    db = models.ForeignKey(DatabaseInfo, verbose_name='数据库', related_name='db_db_db', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='库名', max_length=20)
    # use = models.CharField(verbose_name='用途', max_length=20)
    desc = models.CharField(verbose_name='备注', max_length=100, blank=True, null=True)
    add_user = models.ForeignKey(UserProfile, related_name='db_db_add_user', verbose_name='添加人',
                                 on_delete=models.CASCADE, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    # update_user = models.ForeignKey(UserProfile, related_name='db_db_update_user', verbose_name='修改人',
    #                                 on_delete=models.CASCADE)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((1, '正常'), (0, '停用')), default=1)

    class Meta:
        verbose_name = '数据库库表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return ("%s - %s") % (self.db.host.in_ip, self.name)


######################################
# 数据库用户表
######################################
class DatabaseUserInfo(models.Model):
    db = models.ForeignKey(DatabaseInfo, verbose_name='数据库', related_name='user_db', on_delete=models.CASCADE)
    username = models.CharField(verbose_name='用户名', max_length=20)
    password = models.CharField(verbose_name='密码', max_length=50)
    grant_login = models.CharField(verbose_name='授权登录', max_length=50, default='localhost')
    grant_db = models.ManyToManyField(DatabaseDBInfo, verbose_name='授权库')
    add_user = models.ForeignKey(UserProfile, related_name='user_add_user', verbose_name='添加人',
                                 on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    update_user = models.ForeignKey(UserProfile, related_name='user_update_user', verbose_name='修改人',
                                    on_delete=models.CASCADE)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    desc = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((1, '正常'), (0, '停用')), default=1)

    def get_grant_list(self):
        grant_list = []
        for each in self.grant_db.all():
            grant_list.append(each.id)
        return grant_list

    class Meta:
        verbose_name = '数据库用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return ("%s - %s") % (self.db.host.in_ip, self.username)




