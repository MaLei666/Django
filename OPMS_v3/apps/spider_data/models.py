from django.db import models
from users.models import UserProfile

class PlatformInfo(models.Model):
    name = models.CharField(verbose_name='平台名称', max_length=30)
    logo = models.CharField(verbose_name='logo', max_length=100, blank=True, null=True)
    url = models.CharField(verbose_name='url', max_length=200)
    belong = models.PositiveSmallIntegerField(verbose_name='隶属', choices=((1, '公司平台'), (2, '运维平台'), (3, '其它平台')))
    is_public = models.BooleanField(verbose_name='公开', default=True)
    add_user = models.ForeignKey(UserProfile, verbose_name='添加人', related_name='pl_user', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = '平台表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
