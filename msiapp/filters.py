import django_filters
from django_filters import CharFilter
from .models import Device, Customer


class DeviceFilter(django_filters.FilterSet):
    customers = CharFilter(field_name='customers', lookup_expr='icontains')

    class Meta:
        model = Device
        fields = ['customers']

class CustomerFilter(django_filters.FilterSet):
    customers = CharFilter(field_name='customers', lookup_expr='icontains')
    
    class Meta:
        model = Customer
        fields = ['customers']
