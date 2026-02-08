from django.urls import path
from . import views
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('products/',views.ProductListCreateAPIView.as_view()),
    # path('products/create',views.ProductCreateAPIView.as_view()),
    path('products/<int:product_id>',views.ProductDetailAPIView.as_view()), # we can overide link name to this to refer to this instead of pk key defaultly done by the generic rest_framework
    path('orders/',views.OrderListAPIView.as_view()),
    path('product/info',views.ProductDataAPIView.as_view()),
    path('user-orders/',views.UserOrderListAPIView.as_view(),name='user-orders'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]






# we should add that we reduced the query number and latency time by a lot using silk in django