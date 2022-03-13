import django_filters
from django_filters import CharFilter
from .models import Device, Customer


class DeviceFilter(django_filters.FilterSet):
    customers = CharFilter(field_name='customers', lookup_expr='icontains')

    class Meta:
        model = Device
        fields = ['customers']

class customerFilter(django_filters.FilterSet):
    user = CharFilter(field_name='user', lookup_expr='icontains')
    address_line_1 = CharFilter(field_name='address_line_1', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['user', 'email', 'address_line_1', 'registration_start_date']
