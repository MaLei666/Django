"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from test1.view import index
from django.urls import include, path

urlpatterns = [
    url(r'^admin', admin.site.urls),
    #在url中凡是以url开头的访问都使用index函数来处理该请求
    url(r'^index',index),
    # path('app/', include('test_app.urls')),
    url(r'^app/',include('test_app.urls'))
]

