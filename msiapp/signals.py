from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

from msiapp.views import device
from .models import Customer, Device, DeviceAuthored
import datetime
from datetime import date


@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        # Customer and related customer already being created in view
        Customer.objects.create(
            user=instance,
            registration_start_date=datetime.date.today(),
            added_by_user='System Generated',
        )
        

post_save.connect(customer_profile, sender=User)

@receiver(post_save, sender=Device)
def device_add(sender, instance, created, **kwargs):
    if created:
        customer = Customer.objects.get(id=instance.cus_id)
        instance.customers.add(customer)

       # DeviceAuthored(customer=customer, device=instance).save()

post_save.connect(device_add, sender=Device)
