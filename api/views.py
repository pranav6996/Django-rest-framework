from django.http import JsonResponse
from django.db.models import Max
from .serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer
from .models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view,action
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.views import APIView
from .filters import ProductFilter,InStockFilterBackend,InNameFilterBackend,OrderFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

class ProductListCreateAPIView(generics.ListCreateAPIView):  # this is an advanced versin of serializer and changes it to fucntion to class and get the data
    # queryset=Product.objects.all()
    queryset=Product.objects.order_by('pk') # we use this because of pagination because if we didnt order the data properly it will yeild inconsistent results
    serializer_class=ProductSerializer
    filterset_class=ProductFilter
    filter_backends=[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,InStockFilterBackend,InNameFilterBackend]
    # filter_backends=[filters.SearchFilter]
    search_fields=['name','description']
    ordering_fields=['name','price','stock','description']
    pagination_class=PageNumberPagination
    pagination_class.page_size=10
    pagination_class.page_query_param='pagenum'
    pagination_class.page_size_query_param='size' # this is used to change the page size dynamically by passing the query parameter in the url like ?size=5 and it will display 5 items per page instead of 10 items per page which is the default value we set for pagination class
    pagination_class.max_page_size=5

    def get_permissions(self): 
        self.permission_classes=[AllowAny]
        if self.request.method =='POST':
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()


# the below class is not needed because it is only for creating an api view and not getting the api view so the above class solves it and let us do both get and post using the same apiview

# class ProductCreateAPIView(generics.CreateAPIView):
#     model=Product
#     serializer_class=ProductSerializer

#     def create(self,request,*args,**kwargs):  # this is a inbuilt method and wee are intercepting this to print the data in the middle 
#         print(request.data)
#         return super().create(request,*args,**kwargs)

# @api_view(['GET'])  # this implies the class that this is a api view 
# def product_list(request):  # we use this to display it using the url
#     products=Product.objects.all()
#     serializing=ProductSerializer(products,many=True)  # we used many=True because we are passing a query set which are of multiple objects
# #    return JsonResponse({
# #        'data':serializing.data
# #    }) this is the old way and it is replaced by the blow line
    
    # return Response(serializing.data)




class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):#https://www.django-rest-framework.org/api-guide/generic-views/#retrievedestroyapiview  see in this website for refrence what more we cna keep beside generics. for more permissions and usages
    queryset=Product.objects.all()
    # instead of retrieving all the data like that with all() we can choose a certain field like Product.objects.filter(stock__gt=0)  # here gt indicates greater than
    # we cna also exclude a field like Product.objects.exclude(stock__gt=0) this only returns the products with stock 0
    serializer_class=ProductSerializer
    lookup_url_kwarg='product_id'
    # We did NOT change how DRF searches.
    # DRF still searches using primary key (pk).
    # We only told DRF to read the value from URL param named 'product_id' instead of 'pk'. 

    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method in ['POST','PUT','PATCH','DELETE']:
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()






# @api_view(['GET'])  # this implies the class that this is a api view 
# def product_view(request,pk):  # we use this to display it using the url
#     products=get_object_or_404(Product,pk=pk)
#     serializing=ProductSerializer(products)  # we used many=True because we are passing a query set which are of multiple objects
#     return Response(serializing.data)





#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# class OrderListAPIView(generics.ListAPIView):
#     queryset=Order.objects.prefetch_related('items__product')  
#     serializer_class=OrderSerializer
#     permission_classes=[IsAdminUser]



# WE WILL USE VIEWSETS TO REPLACE THESE CLASSES



# # this shows the data of the specific user that was logged in the website and thier orders
# class UserOrderListAPIView(generics.ListAPIView):
#     queryset=Order.objects.prefetch_related('items__product')    # the double underscore indicates that it fetches both items and items.product we do this for faster fata retreival
#     serializer_class=OrderSerializer
#     permission_classes=[IsAuthenticated]

#     #over riding the queryset
#     def get_queryset(self):
#         qs=super().get_queryset()  # this updates the data dynamically
#         return qs.filter(user=self.request.user)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.prefetch_related('items__product')    # the double underscore indicates that it fetches both items and items.product we do this for faster fata retreival
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    filterset_class=OrderFilter
    filter_backends=[DjangoFilterBackend]

    def get_queryset(self):  #this ensures that the orders of a user is only visisble to them but the admin can see all the orders
        qs=super().get_queryset()
        if not self.request.user.is_staff:
            qs=qs.filter(user=self.request.user)
        return qs
    # this is not used because we wrote the above function and its basically does the same thing
    # @action(detail=False,methods=['get'],url_path='user-orders') # by using this we may get the required data we want similar to get_queryset but this will add in the url like orders/user_orders so it will add more functionality
    # def user_orders(self,request):
    #     orders=self.get_queryset().filter(user=request.user)
    #     serializer=self.get_serializer(orders,many=True)
    #     return Response(serializer.data)


# @api_view(['GET'])
# def order_list(request):
#     orders=Order.objects.prefetch_related(
#         #'items',         we dont need items here because doing items__product already fetches the items fully and then the product
#         'items__product'
#         )  # here items refer to get orderitem for each order and items__product does refer to orderItem by items and get its product
#     serializers=OrderSerializer(orders,many=True)
#     return Response(serializers.data)
  



class ProductDataAPIView(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializers=ProductInfoSerializer({
            'products':products,
            'count':len(products),
            'max_price':products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializers.data)
# @api_view(['GET'])

# def product_data(request):
#     products=Product.objects.all()
#     serializers=ProductInfoSerializer({
#         'products':products,
#         'count':len(products),
#         'max_price':products.aggregate(max_price=Max('price'))['max_price']   #here aggregate will search the database directly for the command kept in the bracket instead of running a function to get the price and calculating the max price and then we use the ['max_price'] again because the aggregate function returns a dict so we extracted the max_price and display the answers
#         #the aggregate is also optimised for database operation in sql
#     })
#     return Response(serializers.data)
