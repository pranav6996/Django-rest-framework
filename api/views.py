from django.http import JsonResponse
from django.db.models import Max
from .serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer
from .models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser


class ProductListAPIView(generics.ListAPIView):  # this is an advanced versin of serializer and changes it to fucntion to class and get the data
    queryset=Product.objects.all()
    serializer_class=ProductSerializer



# @api_view(['GET'])  # this implies the class that this is a api view 
# def product_list(request):  # we use this to display it using the url
#     products=Product.objects.all()
#     serializing=ProductSerializer(products,many=True)  # we used many=True because we are passing a query set which are of multiple objects
# #    return JsonResponse({
# #        'data':serializing.data
# #    }) this is the old way and it is replaced by the blow line
    
    # return Response(serializing.data)




class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    # instead of retrieving all the data like that with all() we can choose a certain field like Product.objects.filter(stock__gt=0)  # here gt indicates greater than
    # we cna also exclude a field like Product.objects.exclude(stock__gt=0) this only returns the products with stock 0
    serializer_class=ProductSerializer
    lookup_url_kwarg='product_id'  # we overrided the primary key to this manually because it automatically used primary key to search so we changed it to check the things






# @api_view(['GET'])  # this implies the class that this is a api view 
# def product_view(request,pk):  # we use this to display it using the url
#     products=get_object_or_404(Product,pk=pk)
#     serializing=ProductSerializer(products)  # we used many=True because we are passing a query set which are of multiple objects
#     return Response(serializing.data)






class OrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product')  
    serializer_class=OrderSerializer
    permission_classes=[IsAdminUser]







# this shows the data of the specific user that was logged in the website and thier orders
class UserOrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product')    # the double underscore indicates that it fetches both items and items.product we do this for faster fata retreival
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    #over rising the queryset
    def get_queryset(self):
        qs=super().get_queryset()  # this updates the data dynamically
        return qs.filter(user=self.request.user)








# @api_view(['GET'])
# def order_list(request):
#     orders=Order.objects.prefetch_related(
#         #'items',         we dont need items here because doing items__product already fetches the items fully and then the product
#         'items__product'
#         )  # here items refer to get orderitem for each order and items__product does refer to orderItem by items and get its product
#     serializers=OrderSerializer(orders,many=True)
#     return Response(serializers.data)
  


@api_view(['GET'])

def product_data(request):
    products=Product.objects.all()
    serializers=ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']   #here aggregate will search the database directly for the command kept in the bracket instead of running a function to get the price and calculating the max price and then we use the ['max_price'] again because the aggregate function returns a dict so we extracted the max_price and display the answers
        #the aggregate is also optimised for database operation in sql
    })
    return Response(serializers.data)


