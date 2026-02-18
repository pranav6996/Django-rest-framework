import django_filters
from .models import Product
from rest_framework import filters


class InStockFilterBackend(filters.BaseFilterBackend):
    #the queryset is already in the class we are keeping this in 
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0) # we can use any filter method here and get the data we want
    
class InNameFilterBackend(filters.BaseFilterBackend):
   

    def filter_queryset(self,request,queryset,view):
        name=request.query_params.get("name")
        if name:
            return queryset.filter(name=name)
        return queryset

class ProductFilter(django_filters.FilterSet):
    # name=django_filters.CharFilter(lookup_expr='icontains')
    # price=django_filters.NumberFilter()
    # price__gt=django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    # price__lt=django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    # instead of these we can directly use it in the way we did for fields object
    class Meta:
        model=Product
        fields={
            "name":["contains","exact"],
            "price":["gt","lt","exact","range"]
        }

