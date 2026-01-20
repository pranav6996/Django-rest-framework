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