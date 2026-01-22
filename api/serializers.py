from rest_framework import serializers
from .models import Product,Order,OrderItem


# a serializer is something that converts the queryset returned by python when fetching data from the backend and convert them into json to display them and do further operations on it
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=(
            'id',
            'name',
            #                 'description',
            'price',
            'stock'
        )
    def validate_price(self,value):  # used to check whether the price is greater than 0 or not
        if value <=0:
            raise serializers.ValidationError(
                "the price should be above 0!!!!"
            )
        return value
# now we are going to write a djangi views.py function to use this class ProductSerializer




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

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True) # this is used to take the data in the OrderItemSerializer and display it inside the same function
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

        






