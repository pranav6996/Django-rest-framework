from django.urls import path
from . import views
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('products/',views.ProductListCreateAPIView.as_view()),
    # path('products/create',views.ProductCreateAPIView.as_view()),
    path('products/<int:product_id>',views.ProductDetailAPIView.as_view()), # we can overide link name to this to refer to this instead of pk key defaultly done by the generic rest_framework
    path('product/info',views.ProductDataAPIView.as_view()),
    # path('orders/',views.OrderListAPIView.as_view()),
    # path('user-orders/',views.UserOrderListAPIView.as_view(),name='user-orders'), # we will use viewsets to replace this

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router=DefaultRouter()
router.register('orders',views.OrderViewSet)
urlpatterns+=router.urls




# we should add that we reduced the query number and latency time by a lot using silk in django