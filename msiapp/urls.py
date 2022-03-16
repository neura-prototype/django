from django.urls import path
from . import views


urlpatterns= [
        path('', views.index, name='index'),
        path('register', views.registerPage, name='register'),
        path('login', views.loginPage, name='login'),
        path('user_profile', views.user_profile, name='user_profile'),
        path('logout', views.logoutUser, name='logout'),
        path('dashboard', views.dashboard, name='dashboard'),
        path('charts', views.charts, name='charts'),

        path('device', views.device, name='device'),
        path('customer_add_device', views.customer_add_device, name='customer_add_device'),
        path('customer_navbar_search', views.customer_navbar_search, name='customer_navbar_search'),
        path('customer_energy_usage_report', views.customer_energy_usage_report, name='customer_energy_usage_report'),
        path('customer_list_device_by_customer', views.customer_list_device_by_customer, name='customer_list_device_by_customer'),
        path('customer_list_customer_by_device', views.customer_list_customer_by_device, name='customer_list_customer_by_device'),
        
        path('list_device', views.list_device, name='list_device'),
        path('edit_device/<str:pk>', views.edit_device, name='edit_device'),
        path('delete_device/<str:pk>', views.delete_device, name='delete_device'),

        path('list_customer', views.list_customer, name='list_customer'),
        # The roll of add customer is played by register in this instance
        path('add_customer', views.add_customer, name='add_customer'),
        path('edit_customer/<str:pk>', views.edit_customer, name='edit_customer'),
        path('delete_customer/<str:pk>', views.delete_customer, name='delete_customer'),

        # ADMIN
        path('enquiry_test', views.enquiry_test, name='enquiry_test'),
        path('admin_navbar_search', views.admin_navbar_search, name='admin_navbar_search'),
        path('admin_user_profile', views.admin_user_profile, name='admin_user_profile'),
        path('admin_energy_usage_report', views.admin_energy_usage_report, name='admin_energy_usage_report'),

        # Admin Device
        path('admin_add_device', views.admin_add_device, name='admin_add_device'),
        path('admin_list_device/<str:pk>', views.admin_list_device, name='admin_list_device'),
        path('admin_edit_device/<str:pk>', views.admin_edit_device, name='admin_edit_device'),
        path('admin_delete_device/<str:pk>', views.admin_delete_device, name='admin_delete_device'),
        path('admin_list_device_by_customer/<str:pk>', views.admin_list_device_by_customer, name='admin_list_device_by_customer'),

        # Admin Customer
        # The roll of add customer is played by register in this instance
        path('admin_add_customer', views.admin_add_customer, name='admin_add_customer'),
        path('admin_list_customer', views.admin_list_customer, name='admin_list_customer'),
        path('admin_edit_customer/<str:pk>', views.admin_edit_customer, name='admin_edit_customer'),
        path('admin_delete_customer/<str:pk>', views.admin_delete_customer, name='admin_delete_customer'),
        path('admin_list_customer_by_device/<str:pk>', views.admin_list_customer_by_device, name='admin_list_customer_by_device'),

]

