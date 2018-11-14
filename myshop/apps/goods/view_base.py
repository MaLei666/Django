from django.views.generic import View
from goods.models import Goods
from rest_framework.pagination import PageNumberPagination
from goods.serializers import GoodsSerializer
from .models import Goods
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics


class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
    '商品列表页'
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

class GoodsPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    #默认每页显示的个数
    page_size = 10
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #页码参数
    page_query_param = 'page'
    #最多能显示多少页
    max_page_size = 100