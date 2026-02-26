from django.db import transaction
from rest_framework import serializers
from .models import Product,Order,OrderItem,User


# a serializer is something that converts the queryset returned by python when fetching data from the backend and convert them into json to display them and do further operations on it


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        # fields=(
        #     'username',
        #     'email',
        #     'is_staff'
        # )
        # fields='__all__'
        #exclude=('password','user_permissions','date_joined') # exclude these fields and displays all like fields
        fields=('password','user_permissions','date_joined','orders')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=(
            'name',
            'description',
            'price',
            'stock'
        )
    def validate_price(self,value):  # used to check whether the price is greater than 0 or not
        if value <=0:
            raise serializers.ValidationError(
                "the price should be above 0!!!!"
            )
        return value
# now we are going to write a django views.py function to use this class ProductSerializer




class OrderItemSerializer(serializers.ModelSerializer):
    #product=ProductSerializer()   # this is to display the full data fields of the class ProductSerializer
    product_name=serializers.CharField(source='product.name')  # we wrote this to refrence the foreign key product and fetch the data of only the product's name and price and return it to print
    product_price=serializers.DecimalField(max_digits=10,decimal_places=2,source='product.price')

    class Meta:
        model=OrderItem
        fields=(
            #'product',
            'quantity',
            #'order'
            'product_name',
            'product_price',
            'item_subtotal',
        )

class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model=OrderItem
            fields=(
                'product','quantity'
            )
    order_id=serializers.UUIDField(read_only=True)
    items=OrderItemCreateSerializer(many=True,required=False)

    def update(self, instance, validated_data):
        orderitem_data=validated_data.pop('items')
        with transaction.atomic():  #basically a fallback approach in databases like it will execute fully or rollback
            instance=super().update(instance,validated_data)

            if orderitem_data is not None:
                instance.items.all().delete()

                for item in orderitem_data:
                    OrderItem.objects.create(order=instance,**item) # instance is that order specifically we are referrring to and we are updating the data of order items in it
        return instance


    def create(self,validated_data):
        orderitem_data=validated_data.pop('items') # this will pop the items key in the dict containing product and quantity and use it neatly to parse the data and post properly
        order=Order.objects.create(**validated_data)

        for item in orderitem_data:
            OrderItem.objects.create(order=order,**item)
        return order
    # we did all this to overide the create function like the post fucntion provided for viewsets and then specified the specific data we had to use for nested data from orders and by adding all them together using the same order_id

    class Meta:
        model=Order
        
        fields=(
            'order_id',
            'user',
            'status',
            'items',
            
        )
        extra_kwargs={
            'user':{'read_only':True} # this is used to make the user field read only because we will automatically assign the user field in the create function using the request.user and we dont want the user to post the user id in the data because it can cause security issues and we want to assign it automatically based on the logged in user
        }

class OrderSerializer(serializers.ModelSerializer):
    order_id=serializers.UUIDField(read_only=True) # we are over riding this because we shouldnt initialise our own order id it should be generated automatically so we use this to remove the order_id field when posting the data
    items=OrderItemSerializer(many=True,read_only=True) # this is used to take the data in the OrderItemSerializer and display it inside the same function ( we removed read_only=True here because we want to post the data)
    total_price=serializers.SerializerMethodField()  # then we should define a function with the name of the initialised variable with get_(name of the variable)

    def get_total_price(self,obj): # here obj refers to the model=Order so it takes the value of Orders
        order_items=obj.items.all()  # we used items here because Order has a relative name of items
        return sum(order_item.item_subtotal for order_item in order_items)  # this runs by running the item_subtotal function in the OrderItem and return the total price of it because we use the price and quantity and multiply it and return the answer
    
    class Meta:
        model=Order
        fields=(
            'order_id',
            'products',
            'user',
            'status',
            'items',
            'total_price',
            
        )

        


class ProductInfoSerializer(serializers.Serializer): # we can not use a meta class because we are not using modelserializer to refrence tl a model and get that data we are just taking a serializer 
    products=ProductSerializer(many=True)
    count=serializers.IntegerField()
    max_price=serializers.FloatField()




