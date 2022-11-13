from cProfile import label
from unicodedata import lookup
import django_filters
from django_filters import CharFilter, NumberFilter, DateFilter
from .models import *


class FarmersFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name='first_name',
                            lookup_expr='icontains', label='First Name')
    second_name = CharFilter(field_name='second_name',
                             lookup_expr='icontains', label='Second Name')
    county = CharFilter(field_name='county', lookup_expr='icontains', label="County")


    class Meta:
        model = Farmer
        fields = ['first_name', 'second_name', 'county']
        
class BuyersFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name='first_name',
                            lookup_expr='icontains', label='First Name')
    second_name = CharFilter(field_name='second_name',
                             lookup_expr='icontains', label='Second Name')
    county = CharFilter(field_name='county', lookup_expr='icontains', label="County")

    class Meta:
        model = Buyer
        fields = ['first_name', 'second_name', 'county']
        
class CountyFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',
                            lookup_expr='icontains', label='Name')
    code = CharFilter(field_name='code',
                             lookup_expr='icontains', label='Code')

    class Meta:
        model = County
        fields = ['name', 'code']
        
class CentreManagerFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',
                            lookup_expr='icontains', label='Name')

    class Meta:
        model = CentreManager
        fields = ['name']

class BlogFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title',
                            lookup_expr='icontains', label='Title')
    class Meta:
        model = Blog
        fields = ['title']




class ProduceFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Name')
    generic_name = CharFilter(field_name='generic_name', lookup_expr='icontains', label='generic name')

    class Meta:
        model = Produce
        fields = ['name', 'generic_name']



class InvoiceFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created',
                            lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='date_created',
                          lookup_expr='lte', label='End Date')

    class Meta:
        model = Invoice
        fields = ['customer', 'status', ]
