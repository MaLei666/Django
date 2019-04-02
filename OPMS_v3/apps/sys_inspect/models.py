######################################
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
# 巡检设备表
######################################
class InspectDevInfo(models.Model):
    platform_id =models.CharField(max_length=45,blank=True,null=True,verbose_name='平台ID')
    dept_id =models.BigIntegerField(verbose_name='部门ID',max_length=20,blank=True,null=True)
    dept_name =models.CharField(max_length=100,blank=True,null=True,verbose_name='部门名称')
    unit_id =models.BigIntegerField(max_length=20,blank=True,null=True,verbose_name='部门ID')
    unit_name=models.CharField(max_length=100,blank=True,null=True,verbose_name='单位名称')
    unit_address=models.CharField(max_length=255,blank=True,null=True,verbose_name='单位地址')
    dev_id =models.CharField(max_length=255,verbose_name='设备ID')
    dev_name =models.CharField(max_length=255,blank=True,null=True,verbose_name='设备名称')
    dev_type =models.CharField(max_length=255,blank=True,null=True,verbose_name='巡检设备类型')
    dev_status = models.IntegerField(verbose_name='设备状态')
    # run_mode =models.IntegerField(verbose_name='设备管理状态')   '0 生产，1 调试，2停用',
    install_position=models.CharField(max_length=255,blank=True,null=True,verbose_name='安装位置')
    create_time=models.DateTimeField(auto_now=True,verbose_name='安装时间')
    update_time =models.DateTimeField(auto_now=True,verbose_name='更新时间')
    update_user =models.CharField(max_length=255,blank=True,null=True,verbose_name='更新者')
    create_mobile =models.CharField(max_length=255,blank=True,null=True,verbose_name='创建用户')
    comment =models.CharField(max_length=1000,verbose_name='备注')
    msg_id =models.CharField(max_length=100,blank=True,null=True,verbose_name='信息ID')
    dev_image1 =models.CharField(max_length=255,blank=True,null=True,verbose_name='设备图片')
    dev_image2 =models.CharField(max_length=255,blank=True,null=True,verbose_name='设备图片')
    dev_image3 =models.CharField(max_length=255,blank=True,null=True,verbose_name='设备图片')
    dev_image4 =models.CharField(max_length=255,blank=True,null=True,verbose_name='设备图片')
    dev_image5 =models.CharField(max_length=255,blank=True,null=True,verbose_name='设备图片')
    dev_image6 =models.CharField(max_length=255,blank=True,null=True,verbose_name='设备图片')
    type1 =models.IntegerField(blank=True,null=True,verbose_name='设备分类1')
    type2 =models.IntegerField(blank=True,null=True,verbose_name='设备分类2')
    type3 =models.IntegerField(blank=True,null=True,verbose_name='设备分类3')
    last_user_id =models.BigIntegerField(max_length=20,blank=True,null=True,verbose_name='最后修改者ID')
    last_user_name =models.CharField(max_length=45,blank=True,null=True,verbose_name='最后修改者名字')
    last_task_id =models.BigIntegerField(max_length=20,blank=True,null=True,verbose_name='最后任务ID')
    last_task_no =models.CharField(max_length=100,blank=True,null=True,verbose_name='最后任务no')
    last_task_name=models.CharField(max_length=200,blank=True,null=True,verbose_name='最后任务名称')
    last_task_time =models.DateTimeField(verbose_name='最后任务时间')
    prev_user_id =models.BigIntegerField(max_length=20,blank=True,null=True,verbose_name='之前修改者ID')
    prev_user_name =models.CharField(max_length=45,blank=True,null=True,verbose_name='之前修改者名字')
    prev_task_id =models.BigIntegerField(max_length=20,blank=True,null=True,verbose_name='之前任务ID')
    prev_task_no =models.CharField(max_length=100,blank=True,null=True,verbose_name='之前任务no')
    prev_task_name =models.CharField(max_length=200,blank=True,null=True,verbose_name='之前任务名称')
    prev_task_time =models.DateTimeField(verbose_name='之前任务时间')
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((1, '正常'), (0, '停用')), default=1)

    class Meta:
        verbose_name = '设备表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.dev_id

#
# ######################################
# # 平台用户表
# ######################################
# class PlatformUserInfo(models.Model):
#     platform = models.ForeignKey(PlatformInfo, verbose_name='平台', related_name='pu_plat', on_delete=models.CASCADE)
#     username = models.CharField(verbose_name='平台名称', max_length=30, blank=True, null=True)
#     password = models.CharField(verbose_name='平台密码', max_length=50, blank=True, null=True)
#     user = models.ForeignKey(UserProfile, verbose_name='用户', related_name='pu_user', on_delete=models.CASCADE)
#     update_user = models.ForeignKey(UserProfile, related_name='platform_update_user', verbose_name='修改人',on_delete=models.CASCADE)
#     update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
#     status = models.PositiveSmallIntegerField(verbose_name='状态', choices=((1, '正常'), (0, '停用')), default=1)
#
#     class Meta:
#         verbose_name = '平台用户表'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return '%s - %s' % (self.platform.name, self.username)





