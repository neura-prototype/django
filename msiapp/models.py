from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User
from msiapp.validators import validate_file_size


class Customer(models.Model):
    GENDER = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # devices = models.ManyToManyField('Device', blank=NULL, null=NULL, through="DeviceAuthored")
    name_1 = models.CharField(max_length=200, blank=NULL, null=NULL)
    name_2 = models.CharField(max_length=200, blank=NULL, null=NULL)
    address_line_1 = models.CharField(max_length=200, blank=NULL, null=NULL)
    address_line_2 = models.CharField(max_length=200, blank=NULL, null=NULL)
    city = models.CharField(max_length=200, blank=NULL, null=NULL)
    province = models.CharField(max_length=200, blank=NULL, null=NULL)
    postal_code = models.CharField(max_length=200, blank=NULL, null=NULL)
    country = models.CharField(max_length=200, blank=NULL, null=NULL)
    gender = models.CharField(max_length=7, blank=NULL, null=NULL, choices=GENDER)
    contact_number = models.CharField(max_length=50, blank=NULL, null=NULL)
    email = models.EmailField(max_length=200, blank=NULL, null=NULL)
    id_number = models.CharField(max_length=50, blank=NULL, null=NULL)
    registration_start_date = models.DateField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='profile_pic', null=True, blank=True, validators=[validate_file_size])
    created_at = models.DateTimeField(auto_now_add=True)
    added_by_user = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user


class Device(models.Model):
    name = models.CharField(max_length=200, blank=NULL, null=NULL)
    address = models.CharField(max_length=200, blank=NULL, null=NULL)
    customers = models.ManyToManyField('Customer', through='DeviceAuthored')
    created_at = models.DateTimeField(auto_now_add=True)
    added_by_user = models.CharField(max_length=255, null=True, blank=True)
    cus_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.customers

class DeviceAuthored(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
