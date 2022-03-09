from multiprocessing import context
from django.shortcuts import render, redirect
from re import X
import mysql.connector
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from .utils import get_plot
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer, Device
from .forms import CreateUserForm, CustomerForm, DeviceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import os
from msi import settings
from .filters import DeviceFilter, CustomerFilter 
from .insert_test import day_django
from datetime import date, timedelta


def enquiry_test(request):
	x = 0
	y = 0
	day_django(x, y)

	'''
	engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/NeuraData')
	period = pd.read_sql("SELECT * FROM vsumperiodvaluesday_django", engine)
	df = pd.DataFrame(period, columns=['DateOnly','EnergyCost'])
	x = []
	y = []
	for column in df:
		columnSeriesObj = df[column]
		if column == 'DateOnly':
			x = columnSeriesObj.values
		elif column == 'EnergyCost':
			y = columnSeriesObj.values
	chart = get_plot(x, y)

	context = {
		'chart', chart,
		}
		'''
	return render(request, '../templates/msiapp_templates/dashboard.html')


def index(request):
  	return render(request, '../templates/msiapp_templates/index.html')


def charts(request):
  	return render(request, '../templates/msiapp_templates/charts.html')


def dashboard(request):
	if request.user.groups == 'customer':
		return render(request, '../templates/msiapp_templates/dashboard.html')
	else:
		customers = Customer.objects.all()

		context = {
			'form': customers,
		}
		return render(request, '../templates/msiapp_templates/admin_folder/customer_list.html', context)


def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, '../templates/accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			messages.success(request, 'User was created for ' + username)

			return redirect('login')

	context = {'form':form}
	return render(request, '../templates/accounts/register.html', context)


@login_required(login_url="login")
def user_profile(request):
	customer = Customer.objects.get(user=request.user)
	if request.method == 'POST':
		customer = CustomerForm(request.POST, request.FILES, instance=customer)
		if customer.is_valid():
			customer = customer.save(commit=False)

			if request.POST.get('address_line_1'):
				customer.address_line_1 = request.POST.get('address_line_1')
			if request.POST.get('address_line_2'):
				customer.address_line_2 = request.POST.get('address_line_2')
			if request.POST.get('city'):
				customer.city = request.POST.get('city')
			if request.POST.get('province'):
				customer.province = request.POST.get('province')
			if request.POST.get('postal_code'):
				customer.postal_code = request.POST.get('postal_code')
			if request.POST.get('country'):
				customer.country = request.POST.get('country')
			if request.POST.get('gender'):
				customer.gender = request.POST.get('gender')
			if request.POST.get('name_1'):
				customer.name_1 = request.POST.get('name_1')
			if request.POST.get('name_2'):
				customer.name_2 = request.POST.get('name_2')
			if request.POST.get('email'):
				customer.email = request.POST.get('email')
			if request.POST.get('contact_number'):
				customer.contact_number = request.POST.get('contact_number')
			if request.POST.get('profile_pic'):
				customer.profile_pic = request.POST.get('profile_pic')
			try:
				customer.profile_pic

				if request.FILES.get('profile_pic'):
					if customer.profile_pic != request.FILES.get('profile_pic') and customer.profile_pic != 'None':
						delete_flag = 1
						delete_path = customer.profile_pic
						customer.profile_pic = request.FILES.get('profile_pic')
					elif customer.profile_pic != request.FILES.get('profile_pic'):
						customer.profile_pic = request.FILES.get('profile_pic')

			except:
				if request.FILES.get('profile_pic'):
					customer.profile_pic = request.FILES.get('profile_pic')
			customer.save()
			if request.FILES.get('profile_pic'):
				# Delete profile pic
				if delete_flag == 1:
					os.remove(settings.MEDIA_ROOT.replace("\media", "\\media\\") + str(delete_path).replace("/", "\\"))

			messages.success(request, "Profile Saved")
			return redirect("dashboard")

		else:
			messages.error(request, "Invalid Form")

	context = {
		'form': customer
	}
	delete_flag = 0
	return render(request, "msiapp_templates/user_profile.html", context)


#def device(request):
#
#  return render(request, '../templates/msiapp_templates/device_add.html')

@login_required(login_url="login")
def device(request):
	device = ''
	if request.method == 'POST':

		device = DeviceForm(request.POST, request.FILES)
		customer = Customer.objects.get(user=request.user)
		if device.is_valid():
			Device.objects.create(
				name = request.POST.get('name'),
				address = request.POST.get('address'),
				added_by_user = 'System Generated',
				cus_id = customer.id
			)
			# Goes to signals.py after saving Device.
			messages.success(request, "Device Saved")
			return redirect("list_device")

		else:
			messages.error(request, "Invalid Form, Device Add Failed")

	context = {
		'form': device
	}
	delete_flag = 0
	return render(request, '../templates/msiapp_templates/device_add.html')


@login_required(login_url="login")
def list_device(request):
	user = request.user
	try:
		customer = Customer.objects.get(user=user)
	# 	print(customer)
	except:
		print('except')
	device = Device.objects.filter(customers=customer)
	check = len(device)
	print('check', check)
	if check == 0:
		return redirect('device')

	my_filter = DeviceFilter(request.GET, queryset=device)
	meetings = my_filter.qs
	context = {
        'myFilter': my_filter,
        'form': meetings,
    }
	return render(request, '../templates/msiapp_templates/device_list.html', context)


def edit_device(request, pk):
	pass


def delete_device(request, pk):
	pass


def admin_dashboard(request):
	return render(request, '../templates/msiapp_templates/admin_folder/admin_dashboard.html')


def customer_list(request):
	customers = Customer.objects.all()
	return customers
	#context = {
	#'form': customers,
	#}
	#return render(request, '../templates/msiapp_templates/admin_folder/customer_list.html')


def admin_navbar_search(request):
	if request.method == 'POST':
		node_name = float(request.POST.get('node_name'))
		print('type', type(node_name))
		start_date = request.POST.get('start_date')
		print(start_date)
		# Change date for MySQL
		start_date = start_date.replace('-','/')

		end_date = request.POST.get('end_date')
		print(end_date)
		# Change date for MySQL
		end_date = end_date.replace('-','/')
		print('node_name', node_name)
		engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/NeuraData')
		period = pd.read_sql("SELECT * FROM vsumperiodvaluesday_django", engine)
		node_period = period[(period['Node'] == node_name)]
		print('node_period', node_period)
		new_period = node_period[(node_period['DateOnly'] >= start_date) & (node_period['DateOnly'] <= end_date)]
		
		print('new_period', new_period)
		df = pd.DataFrame(new_period, columns=['DateOnly','EnergyCost'])
		x = []
		y = []
		for column in df:
			columnSeriesObj = df[column]
			if column == 'DateOnly':
				x = columnSeriesObj.values
			elif column == 'EnergyCost':
				y = columnSeriesObj.values
		chart = get_plot(x, y)
		df.plot(x ='DateOnly', y='EnergyCost', kind = 'line')
		#plt.show()
		return render(request, '../templates/msiapp_templates/admin_folder/energy_price.html', {'chart':chart})
