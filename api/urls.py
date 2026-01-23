from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.product_list),
    path('products/<int:pk>',views.product_view),
    path('orders/',views.order_list),
    path('product/info',views.product_data),

    
    
]






# we should add that we reduced the query number and latency time by a lot using silk in django