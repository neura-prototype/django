# importing group class from django
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
 
# import User model
from users.models import User
 
new_group, created = Group.objects.get_or_create(name ='new_group')
 
# Code to add permission to group
ct = ContentType.objects.get_for_model(User)
 
# If I want to add 'Can go Haridwar' permission to level0 ?
permission = Permission.objects.create(codename ='can_go_haridwar',
                                        name ='Can go to Haridwar',
                                                content_type = ct)
new_group.permissions.add(permission)