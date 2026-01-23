from django.http import JsonResponse
from django.db.models import Max
from .serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer
from .models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404



@api_view(['GET'])  # this implies the class that this is a api view 
def product_list(request):  # we use this to display it using the url
    products=Product.objects.all()
    serializing=ProductSerializer(products,many=True)  # we used many=True because we are passing a query set which are of multiple objects
#    return JsonResponse({
#        'data':serializing.data
#    }) this is the old way and it is replaced by the blow line
    
    return Response(serializing.data)


@api_view(['GET'])  # this implies the class that this is a api view 
def product_view(request,pk):  # we use this to display it using the url
    products=get_object_or_404(Product,pk=pk)
    serializing=ProductSerializer(products)  # we used many=True because we are passing a query set which are of multiple objects
    return Response(serializing.data)

@api_view(['GET'])
def order_list(request):
    orders=Order.objects.all()
    serializers=OrderSerializer(orders,many=True)
    return Response(serializers.data)
  


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


