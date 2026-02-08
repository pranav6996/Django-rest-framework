from django.contrib import admin
from .models import Order,OrderItem,User
# Register your models here.


#instead of seeing and adding data seperatly for Order and OrderItem we do this so that we can add the data of both at the same time without switching tabs
#This makes OrderItem editable inside Order admin page.
class OrderItemInLine(admin.TabularInline):
    model=OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines=[
        OrderItemInLine
    ]

admin.site.register(Order,OrderAdmin)
admin.site.register(User)
#this line integrates order table in the admin page and it will link OrderItem in it because we kept the inlines of it in the class


