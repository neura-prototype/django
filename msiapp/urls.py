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
        path('list_device', views.list_device, name='list_device'),
        path('edit_device/<str:pk>', views.edit_device, name='edit_device'),
        path('delete_device/<str:pk>', views.delete_device, name='delete_device'),
        path('enquiry_test', views.enquiry_test, name='enquiry_test'),
]
