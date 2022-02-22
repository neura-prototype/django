# Generated by Django 4.0.2 on 2022-02-15 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import msiapp.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_1', models.CharField(blank=0, max_length=200, null=0)),
                ('name_2', models.CharField(blank=0, max_length=200, null=0)),
                ('address_line_1', models.CharField(blank=0, max_length=200, null=0)),
                ('address_line_2', models.CharField(blank=0, max_length=200, null=0)),
                ('city', models.CharField(blank=0, max_length=200, null=0)),
                ('province', models.CharField(blank=0, max_length=200, null=0)),
                ('postal_code', models.CharField(blank=0, max_length=200, null=0)),
                ('country', models.CharField(blank=0, max_length=200, null=0)),
                ('gender', models.CharField(blank=0, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], max_length=7, null=0)),
                ('contact_number', models.CharField(blank=0, max_length=50, null=0)),
                ('email', models.EmailField(blank=0, max_length=200, null=0)),
                ('id_number', models.CharField(blank=0, max_length=50, null=0)),
                ('registration_start_date', models.DateField(auto_now_add=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic', validators=[msiapp.validators.validate_file_size])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('added_by_user', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=0, max_length=200, null=0)),
                ('address', models.CharField(blank=0, max_length=200, null=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('added_by_user', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceAuthored',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msiapp.customer')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msiapp.device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='customers',
            field=models.ManyToManyField(through='msiapp.DeviceAuthored', to='msiapp.Customer'),
        ),
        migrations.AddField(
            model_name='customer',
            name='devices',
            field=models.ManyToManyField(through='msiapp.DeviceAuthored', to='msiapp.Device'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterOrderWithRespectTo(
            name='device',
            order_with_respect_to='customers',
        ),
        migrations.AlterOrderWithRespectTo(
            name='customer',
            order_with_respect_to='devices',
        ),
    ]
