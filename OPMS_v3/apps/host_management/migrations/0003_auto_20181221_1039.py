# Generated by Django 2.0.6 on 2018-12-21 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('host_management', '0002_auto_20181108_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainNameInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], default=1, verbose_name='状态')),
                ('add_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dom_add_user', to=settings.AUTH_USER_MODEL, verbose_name='添加人')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dom_update_user', to=settings.AUTH_USER_MODEL, verbose_name='修改人')),
            ],
            options={
                'verbose_name': '域名表',
                'verbose_name_plural': '域名表',
            },
        ),
        migrations.CreateModel(
            name='DomainNameResolveInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='二级域名')),
                ('ip', models.GenericIPAddressField(verbose_name='IP地址')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], default=1, verbose_name='状态')),
                ('add_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dom_res_add_user', to=settings.AUTH_USER_MODEL, verbose_name='添加人')),
                ('domain_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host_management.DomainNameInfo', verbose_name='域名')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dom_res_update_user', to=settings.AUTH_USER_MODEL, verbose_name='修改人')),
            ],
            options={
                'verbose_name': '域名解析表',
                'verbose_name_plural': '域名解析表',
            },
        ),
        migrations.CreateModel(
            name='OperatingSystemInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='系统名称')),
                ('version', models.CharField(max_length=10, verbose_name='系统版本')),
                ('bit', models.PositiveSmallIntegerField(choices=[(32, '32位'), (64, '64位')], default=64, verbose_name='位数')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='描述')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], verbose_name='状态')),
                ('add_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='os_add_user', to=settings.AUTH_USER_MODEL, verbose_name='添加人')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='os_update_user', to=settings.AUTH_USER_MODEL, verbose_name='修改人')),
            ],
            options={
                'verbose_name': '操作系统',
                'verbose_name_plural': '操作系统',
            },
        ),
        migrations.CreateModel(
            name='PortToPortInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_out', models.GenericIPAddressField(blank=True, null=True, verbose_name='公网 IP')),
                ('port_out', models.IntegerField(verbose_name='外网端口')),
                ('ip_in', models.GenericIPAddressField(verbose_name='内网 IP')),
                ('port_in', models.IntegerField(verbose_name='内网端口')),
                ('use', models.CharField(max_length=20, verbose_name='用途')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], default=1, verbose_name='状态')),
                ('add_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='port_add_user', to=settings.AUTH_USER_MODEL, verbose_name='添加人')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='port_update_user', to=settings.AUTH_USER_MODEL, verbose_name='修改人')),
            ],
            options={
                'verbose_name': '端口映射表',
                'verbose_name_plural': '端口映射表',
            },
        ),
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='项目名称')),
                ('run_env', models.CharField(max_length=100, verbose_name='运行环境')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], verbose_name='状态')),
                ('add_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pro_add_user', to=settings.AUTH_USER_MODEL, verbose_name='添加人')),
                ('op_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pro_op_user', to=settings.AUTH_USER_MODEL, verbose_name='运维人员')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pro_update_user', to=settings.AUTH_USER_MODEL, verbose_name='修改人')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
            },
        ),
        migrations.CreateModel(
            name='UseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='用途')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='描述')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用')], verbose_name='状态')),
                ('add_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='use_add_user', to=settings.AUTH_USER_MODEL, verbose_name='添加人')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='use_update_user', to=settings.AUTH_USER_MODEL, verbose_name='修改人')),
            ],
            options={
                'verbose_name': '用途',
                'verbose_name_plural': '用途',
            },
        ),
        migrations.AddField(
            model_name='hostinfo',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='host_management.ProjectInfo', verbose_name='项目'),
        ),
        migrations.AddField(
            model_name='hostinfo',
            name='system',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='host_management.OperatingSystemInfo', verbose_name='操作系统'),
        ),
        migrations.AddField(
            model_name='hostinfo',
            name='use',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='host_management.UseInfo', verbose_name='用途'),
        ),
    ]