
# from django.contrib import admin
from django.urls import path,include,re_path
import xadmin
from django.views.static import serve
from myshop.settings import MEDIA_ROOT
from goods.view_base import GoodsListView
from rest_framework.documentation import include_docs_urls
from goods.views import GoodsListViewSet,CategoryViewSet,BannerViewset,IndexCategoryViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from users.views import UserViewset
from user_operation.views import UserFavViewset,LeavingMessageViewset,AddressViewset

router = DefaultRouter()
#配置goods的url
router.register(r'goods', GoodsListViewSet)
# 配置Category的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")
#配置用户的url
router.register(r'users', UserViewset, base_name="users")
# 配置用户收藏的url
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
# 配置用户留言的url
router.register(r'messages', LeavingMessageViewset, base_name="messages")
# 配置收货地址
router.register(r'address',AddressViewset , base_name="address")
# 配置首页轮播图的url
router.register(r'banners', BannerViewset, base_name="banners")
# 首页系列商品展示url
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
# 富文本编辑器url
    path('ueditor/',include('DjangoUeditor.urls' )),
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),
    path('goods/',GoodsListView.as_view(),name='goods-list'),
    # drf文档，title自定义
    path('docs',include_docs_urls(title='使用文档')),
    path('api-auth/',include('rest_framework.urls')),
    #商品列表页
    re_path('^', include(router.urls)),
    # token
    path('api-token-auth/', views.obtain_auth_token),
    # jwt的token认证接口
    # path('jwt-auth/', obtain_jwt_token ),
    # jwt的认证接口
    path('login/', obtain_jwt_token ),
]
