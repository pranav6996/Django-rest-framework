from django.http import JsonResponse
from .serializers import ProductSerializer
from .models import Product
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

