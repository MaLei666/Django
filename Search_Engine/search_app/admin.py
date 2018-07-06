from django.contrib import admin
from search_app.models import User

# Register your models here.
class HostAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'age',
        'birthday',
        'gender',
        'account',
    ]
    search_fields = ('name',)

admin.site.register(User,HostAdmin)
admin.AdminSite.site_header='运维系统管理后台'
admin.AdminSite.site_title='运维系统'