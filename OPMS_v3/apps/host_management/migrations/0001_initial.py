# Generated by Django 2.0.6 on 2018-11-08 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseDBInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='库名')),
                ('desc', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], default=1, verbose_name='状态')),
            ],
            options={
                'verbose_name': '数据库库表',
                'verbose_name_plural': '数据库库表',
            },
        ),
        migrations.CreateModel(
            name='DatabaseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='数据库名称')),
                ('db_version', models.CharField(blank=True, max_length=20, null=True, verbose_name='数据库版本')),
                ('db_admin_user', models.CharField(max_length=20, verbose_name='数据库管理员')),
                ('db_admin_pass', models.CharField(max_length=50, verbose_name='数据库管理员密码')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], default=1, verbose_name='状态')),
            ],
            options={
                'verbose_name': '数据库信息',
                'verbose_name_plural': '数据库信息',
            },
        ),
        migrations.CreateModel(
            name='DatabaseUserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('grant_login', models.CharField(default='localhost', max_length=50, verbose_name='授权登录')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], default=1, verbose_name='状态')),
            ],
            options={
                'verbose_name': '数据库用户表',
                'verbose_name_plural': '数据库用户表',
            },
        ),
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_ip', models.GenericIPAddressField(verbose_name='内网IP')),
                ('out_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='外网IP')),
                ('hostname', models.CharField(max_length=30, verbose_name='主机名')),
                ('ssh_port', models.IntegerField(null=True, verbose_name='远程端口')),
                ('root_ssh', models.BooleanField(default=True, verbose_name='是否允许 root 远程')),
                ('admin_user', models.CharField(max_length=20, verbose_name='管理员用户')),
                ('admin_pass', models.CharField(max_length=50, verbose_name='管理员密码')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], default=1, verbose_name='状态')),
            ],
            options={
                'verbose_name': '主机信息',
                'verbose_name_plural': '主机信息',
            },
        ),
        migrations.CreateModel(
            name='HostServiceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='服务名称')),
                ('version', models.CharField(blank=True, max_length=20, null=True, verbose_name='服务版本')),
                ('listen_user', models.CharField(max_length=20, verbose_name='监听用户')),
                ('listen_port', models.CharField(max_length=30, verbose_name='监听端口')),
                ('ins_path', models.CharField(max_length=100, verbose_name='安装路径')),
                ('log_path', models.CharField(blank=True, max_length=100, null=True, verbose_name='日志路径')),
                ('backup_path', models.CharField(blank=True, max_length=100, null=True, verbose_name='备份路径')),
                ('start_cmd', models.CharField(max_length=100, verbose_name='启动命令')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], verbose_name='状态')),
            ],
            options={
                'verbose_name': '主机服务信息',
                'verbose_name_plural': '主机服务信息',
            },
        ),
    ]