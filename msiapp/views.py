from multiprocessing import context
from django.shortcuts import render, redirect
from re import X
import mysql.connector
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from .utils import get_plot, get_usage_plot
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer, Device, DeviceAuthored
from .forms import CreateUserForm, CustomerForm, DeviceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
import os
from msi import settings
from .filters import DeviceFilter, customerFilter 
from .insert_test import day_django
from datetime import date, timedelta, datetime
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test


@login_required(login_url="login")
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


@login_required(login_url="login")
def dashboard(request):
	
	if request.user.groups.filter(name='admin').exists():
		customers = Customer.objects.all()
		# Paginator
		page_num = request.GET.get('page', 1)
		paginator = Paginator(customers, 6) # 6 customers per page
		print(paginator)
		try:
			customers = paginator.page(page_num)
		except PageNotAnInteger:
			# if page is not an integer, deliver the first page
			customers = paginator.page(1)
		except EmptyPage:
			# if the page is out of range, deliver the last page
			customers = paginator.page(paginator.num_pages)

		context = {
			'form': customers,
			'page_obj': customers,
		}
		return render(request, '../templates/msiapp_templates/admin_folder/admin_customer_list.html', context)					
	elif request.user.groups.filter(name='customer').exists():
		return render(request, '../templates/msiapp_templates/dashboard.html')
	else:
		customers = Customer.objects.all()
		# Paginator
		page_num = request.GET.get('page', 1)
		paginator = Paginator(customers, 6) # 6 customers per page
		print(paginator)
		try:
			customers = paginator.page(page_num)
		except PageNotAnInteger:
			# if page is not an integer, deliver the first page
			customers = paginator.page(1)
		except EmptyPage:
			# if the page is out of range, deliver the last page
			customers = paginator.page(paginator.num_pages)

		context = {
			'form': customers,
			'page_obj': customers,
		}
		return render(request, '../templates/msiapp_templates/admin_folder/admin_customer_list.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			my_user = User.objects.get(username=user)
			print(my_user.id)
			customer = Customer.objects.get(user=my_user)

			if customer.name_1:

				if user.groups.filter(name='admin').exists():
					return redirect('admin_list_customer')
				elif user.groups.filter(name='customer').exists():
					return render(request, '../templates/msiapp_templates/dashboard.html')
				else:
					return redirect('admin_list_customer')
			else:
				# print('request.user.user_groups', request.user.user_groups)
				print('request.user', request.user)
				#if request.user.groups == 'customer':
				if user.groups.filter(name='admin').exists():
					return redirect('admin_user_profile')
				elif user.groups.filter(name='customer').exists():
					return redirect('user_profile')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, '../templates/accounts/login.html', context)


@login_required(login_url="login")
def logoutUser(request):
	logout(request)
	return redirect('login')


######################################
# This is actually add customer html #
######################################
def is_admin(user):
    try:
        return user.is_authenticated and user.groups.filter(name='admin').exists()
    except User.DoesNotExist:
        return False


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			my_admin_flag = request.POST.get('is_admin')
			if my_admin_flag == 'customer':
				group = Group.objects.get(name='customer')
				user.groups.add(group)
			elif my_admin_flag == 'admin':
				group = Group.objects.get(name='admin')
				user.groups.add(group)
			else:
				pass

			my_email = []
			messages.success(request, 'User was created for ' + username)
			my_username = request.POST.get('username')
			my_email = str(request.POST.get('email'))
			my_password = request.POST.get('password1')
			print(my_email)
			# Send Email via code
			send_mail(
				'Neura Email Verification',
				'Please click link and login to complete Registration process. http://127.0.0.1:8000/login',
				'sparDjango"gmail.com',
				[my_email],
				fail_silently=False,
			)
			if request.user.groups == 'customer':
				return redirect('list_customer')
			else:
				return redirect('admin_list_customer')
		else:
			my_username = request.POST.get('username')
			my_email = request.POST.get('email')
			context = {
				'form': form,
				'my_username': my_username,
				'my_email': my_email,
				}
			messages.error(request, "Username Already Exists")
			return render(request, "msiapp_templates/admin_folder/admin_customer_add.html", context)
	else:

		context = {
					'form': form,
					}
		return redirect('admin_list_customer')


@login_required(login_url="login")
def user_profile(request):
	customer = Customer.objects.get(user=request.user)
	if request.method == 'POST':
		customer = CustomerForm(request.POST, request.FILES, instance=customer)
		if customer.is_valid():
			customer = customer.save(commit=False)
			customer.user = request.user
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
			
			customer.email = request.user.email
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


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_user_profile(request):
	customer = Customer.objects.get(user=request.user)
	if request.method == 'POST':
		customer = CustomerForm(request.POST, request.FILES, instance=customer)
		if customer.is_valid():
			customer = customer.save(commit=False)
			customer.user = request.user
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
			
			customer.email = request.user.email
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
	return render(request, "msiapp_templates/admin_folder/admin_user_profile.html", context)


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
				cus_id = request.POST.get('customer_id'),
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
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_add.html')


@login_required(login_url="login")
def customer_add_device(request):
	device = ''
	if request.method == 'POST':
		user = request.user
		try:
			user = User.objects.get(username=user)
		except:
			messages.warning(request, 'User does not exist. Please check username')
			return redirect('customer_add_device')
		
		device = DeviceForm(request.POST, request.FILES)
		customer = Customer.objects.get(user=request.user)
		if device.is_valid():
			Device.objects.create(
				name = request.POST.get('name'),
				address = request.POST.get('address'),
				added_by_user = request.user,
				cus_id = customer.id,
			)
			# Goes to signals.py after saving Device.
			messages.success(request, "Device Saved")
			print('yo yo')
			return redirect("list_device")

		else:
			messages.error(request, "Invalid Form, Device Add Failed")

	context = {
		'form': device
	}
	delete_flag = 0
	return render(request, '../templates/msiapp_templates/customer_device_add.html')


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_add_device(request):
	device = ''
	if request.method == 'POST':
		user = request.POST.get('customer_id')
		try:
			user = User.objects.get(username=user)
		except:
			messages.warning(request, 'User does not exist. Please check username')
			return redirect('admin_add_device')

		device = DeviceForm(request.POST, request.FILES)
		customer = Customer.objects.get(user=user)
		
		if device.is_valid():
			Device.objects.create(
				name = request.POST.get('name'),
				address = request.POST.get('address'),
				added_by_user = request.user.username,
				cus_id = customer.id,
			)
			# Goes to signals.py after saving Device.
			messages.success(request, "Device Saved")
			return redirect("admin_list_device", pk=user.id)

		else:
			messages.error(request, "Invalid Form, Device Add Failed")

	context = {
		'form': device
	}
	delete_flag = 0
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_add.html')


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
	return render(request, '../templates/msiapp_templates/customer_device_list.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_list_device(request, pk):
	if request.method == 'POST':
		device = Device.objects.filter(customers=customer)
		check = len(device)
		if check == 0:
			messages.error(request, "Device not found... ")
			return redirect(admin_list_customer)

		my_filter = DeviceFilter(request.GET, queryset=device)
		meetings = my_filter.qs
		context = {
			'myFilter': my_filter,
			'form': meetings,
			'customer': customer,
		}
		return render(request, '../templates/msiapp_templates/admin_folder/admin_device_list.html', context)
	else:
		devices = Device.objects.all()
		context = {
			'form': devices,
		}
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_list.html', context)


@login_required(login_url="login")
def edit_device(request, pk):
	device_name = pk

	try:
		device = Device.objects.get(name=device_name)
		# print(customer)
	except:
		# Goes to signals.py after saving Device.
		messages.error(request, "Device not found!")
		# Redirect to the same page
		return redirect(edit_device, id)
	if request.method == 'POST':
		pass

	context = {
        'form': device,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_edit.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_edit_device(request, pk):
	device_name = pk
	try:
		device = Device.objects.get(id=device_name)
		#print(customer)
		
	except:
		# Goes to signals.py after saving Device.
		messages.error(request, "Device not found!")
		# Redirect to the same page
		return redirect(edit_device, id)
	
	# Many to many search
	deviceAuthored = DeviceAuthored.objects.get(device=device)
	customer_device = deviceAuthored.customer.user.username
	if request.method == 'POST':
		if request.POST.get('name'):
			device.name = request.POST.get('name')
		if request.POST.get('address'):
			device.address = request.POST.get('address')
		#if request.POST.get('customers'):
			# device.customers = request.POST.get('customers')
			# device.customers.set(device)
		device.save()
		messages.success(request, "Device edit saved")
		return redirect(admin_list_device, pk=deviceAuthored.customer.user.id)

	context = {
        'form': device,
		'customer_device': customer_device,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_edit.html', context)


@login_required(login_url="login")
def delete_device(request, pk):
	pass


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_delete_device(request, pk):
	device = Device.objects.get(id=pk)
	device_id = device.id
	device_authored = DeviceAuthored.objects.get(device=device)
	customer = device_authored.customer
	device.delete()
	messages.success(request, "Device deleted :  " + str(device_id))
	# Redirect to the same page
	return redirect(admin_list_device, pk=customer.user.id)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_dashboard(request):
	return render(request, '../templates/msiapp_templates/admin_folder/admin_dashboard.html')


@login_required(login_url="login")
def list_customer(request):
	customers = Customer.objects.all()
	initial_customer_count = customers.count()
	myFilter = customerFilter(request.GET, queryset=customers)
	# rebuilt list

	customers = myFilter.qs

	user = request.GET.get('user')
	email = request.GET.get('email')
	address_line_1 = request.GET.get('address_line_1')
	registration_start_date = request.GET.get('registration_start_date')

	if user == None:
		user = ''
	if email == None:
		email = ''
	if address_line_1 == None:
		address_line_1 = ''
	if registration_start_date == None:
		registration_start_date = ''

	context = {
	'form': customers,
	'user': user,
	'email': email,
	'address_line_1': address_line_1,
	'registration_start_date': registration_start_date,
	}
	return render(request, '../templates/msiapp_templates/customer_list.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_list_customer(request):
	customers = Customer.objects.all()
	initial_customer_count = customers.count()

	myFilter = customerFilter(request.GET, queryset=customers)
	
	# rebuilt list
	customers = myFilter.qs

	# Paginator
	page_num = request.GET.get('page', 1)
	paginator = Paginator(customers, 6) # 6 customers per page

	try:
		customers = paginator.page(page_num)
	except PageNotAnInteger:
		# if page is not an integer, deliver the first page
		customers = paginator.page(1)
	except EmptyPage:
		# if the page is out of range, deliver the last page
		customers = paginator.page(paginator.num_pages)

	name_1 = request.GET.get('name_1')
	email = request.GET.get('email')
	address_line_1 = request.GET.get('address_line_1')
	registration_start_date = request.GET.get('registration_start_date')

	if name_1 == None:
		name_1 = ''
	if email == None:
		email = ''
	if address_line_1 == None:
		address_line_1 = ''
	if registration_start_date == None:
		registration_start_date = ''
	print('count', customers)
	context = {
		'form': customers,
		'page_obj': customers,
		'name_1': name_1,
		'email': email,
		'address_line_1': address_line_1,
		'registration_start_date': registration_start_date,
	}
	return render(request, '../templates/msiapp_templates/admin_folder/admin_customer_list.html', context)


@login_required(login_url="login")
def add_customer(request):
	customers = Customer.objects.all()

	context = {
	'form': customers,
	}
	return render(request, '../templates/msiapp_templates/customer_add.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_add_customer(request):
	customers = Customer.objects.all()

	context = {
	'form': customers,
	}
	return render(request, '../templates/msiapp_templates/admin_folder/admin_customer_add.html', context)


@login_required(login_url="login")
def edit_customer(request, pk):
	customers = Customer.objects.all()

	context = {
	'form': customers,
	}
	return render(request, '../templates/msiapp_templates/customer_add.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_edit_customer(request, pk):
	customers = Customer.objects.all()

	context = {
	'form': customers,
	}
	return render(request, '../templates/msiapp_templates/admin_folder/admin_customer_add.html', context)


@login_required(login_url="login")
def delete_customer(request, pk):
	customers = Customer.objects.all()

	context = {
	'form': customers,
	}
	return render(request, '../templates/msiapp_templates/customer_add.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_delete_customer(request, pk):
	customers = Customer.objects.all()

	context = {
	'form': customers,
	}
	return render(request, '../templates/msiapp_templates/admin_folder/admin_customer_add.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_navbar_search(request):

	if request.method == 'POST':
		node_name = float(request.POST.get('node_name'))
		start_date = request.POST.get('start_date')
		end_date = request.POST.get('end_date')

		engine = create_engine('mysql+mysqlconnector://Quinn:Holland$1@neura.dyndns.org:3306/NeuraData')
		# period = pd.read_sql("SELECT * FROM vsumperiodvaluesday", engine)
		period = pd.read_sql("SELECT * FROM NeuraData.vsumperiodvaluesdayEnergy", engine)

		node_period = period[(period['Node'] == node_name)]
		#'''
		if start_date == '' and end_date != '':

			# Change date for MySQL
			if end_date:
				end_date = end_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] <= end_date)]

		elif start_date != '' and end_date != '':
			# Change date for MySQL
			if start_date:
				start_date = start_date.replace('-','/')
			# Change date for MySQL
			if end_date:
				end_date = end_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] >= start_date) & (node_period['DateOnly'] <= end_date)]
		elif end_date == '' and start_date != '':
			print('if_3')
			# Change date for MySQL
			start_date = start_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] >= start_date)]
		else:
			
			new_period = node_period
		print(new_period)
		# To display dataframe
		table_content = new_period.to_html()
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
		context = {
			'chart':chart,
			'table_content': table_content,
		}
		return render(request, '../templates/msiapp_templates/admin_folder/admin_energy_price.html', context)
	else:
		customers = ''

		context = {
			'form': customers,
		}
		return render(request, '../templates/msiapp_templates/admin_folder/admin_energy_price.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_energy_usage_report(request):
	if request.method == 'POST':
		node_name = float(request.POST.get('node_name'))
		start_date = request.POST.get('start_date')
		end_date = request.POST.get('end_date')

		engine = create_engine('mysql+mysqlconnector://Quinn:Holland$1@neura.dyndns.org:3306/NeuraData')
		# period = pd.read_sql("SELECT * FROM vsumperiodvaluesday", engine)
		period = pd.read_sql("SELECT * FROM NeuraData.vsumperiodvaluesdayEnergy", engine)

		node_period = period[(period['Node'] == node_name)]
		#'''
		if start_date == '' and end_date != '':

			# Change date for MySQL
			if end_date:
				end_date = end_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] <= end_date)]

		elif start_date != '' and end_date != '':
			# Change date for MySQL
			if start_date:
				start_date = start_date.replace('-','/')
			# Change date for MySQL
			if end_date:
				end_date = end_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] >= start_date) & (node_period['DateOnly'] <= end_date)]
		elif end_date == '' and start_date != '':
			print('if_3')
			# Change date for MySQL
			start_date = start_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] >= start_date)]
		else:
			
			new_period = node_period
		print(new_period)
		# To display dataframe
		table_content = new_period.to_html()
		df = pd.DataFrame(new_period, columns=['DateOnly','Energy'])
		x = []
		y = []
		for column in df:
			columnSeriesObj = df[column]
			if column == 'DateOnly':
				x = columnSeriesObj.values
			elif column == 'Energy':
				y = columnSeriesObj.values
		chart = get_usage_plot(x, y)
		df.plot(x ='DateOnly', y='Energy', kind = 'line')
		context = {
			'chart':chart,
			'table_content': table_content,
		}
		return render(request, '../templates/msiapp_templates/admin_folder/admin_energy_usage.html', context)
	else:
		customers = ''

		context = {
			'form': customers,
		}
		return render(request, '../templates/msiapp_templates/admin_folder/admin_energy_usage.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_list_device_by_customer(request, pk):
	user = pk
	try:
		customer = Customer.objects.get(user=user)
	# 	print(customer)
	except:
		messages.error(request, 'No Device Present. Please Add New Device')
		return redirect('device')
	device = Device.objects.filter(customers=customer)
	check = len(device)

	if check == 0:
		messages.warning(request, 'No Devices Linked To Customer. Please Add Device')
		return redirect('device')

	my_filter = DeviceFilter(request.GET, queryset=device)
	meetings = my_filter.qs
	context = {
        'myFilter': my_filter,
        'form': meetings,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_list_by_customer.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_list_customer_by_device(request, pk):
	customers = []
	print(pk)
	try:
		devices = Device.objects.filter(name=pk)
		print(len(devices))
	except:
		messages.warning(request, 'No Device Present. Please Create Device')
		return redirect('device')

	#my_filter = Device(request.GET, queryset=devices)
	# meetings = devices.qs

	context = {
        'myFilter': devices,
        'form': devices,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_list_customer_by_device.html', context)

#
@login_required(login_url="login")
def customer_navbar_search(request):
	if request.method == 'POST':
		node_name = float(request.POST.get('node_name'))
		start_date = request.POST.get('start_date')
		end_date = request.POST.get('end_date')

		engine = create_engine('mysql+mysqlconnector://Quinn:Holland$1@neura.dyndns.org:3306/NeuraData')
		# period = pd.read_sql("SELECT * FROM vsumperiodvaluesday", engine)
		period = pd.read_sql("SELECT * FROM NeuraData.vsumperiodvaluesdayEnergy", engine)

		node_period = period[(period['Node'] == node_name)]
		#'''
		if start_date == '' and end_date != '':
			print('if_1')
			# Change date for MySQL
			if end_date:
				end_date = end_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] <= end_date)]

		elif start_date != '' and end_date != '':
			print('if_2')
			# Change date for MySQL
			if start_date:
				start_date = start_date.replace('-','/')
			# Change date for MySQL
			if end_date:
				end_date = end_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] >= start_date) & (node_period['DateOnly'] <= end_date)]
		elif end_date == '' and start_date != '':
			print('if_3')
			# Change date for MySQL
			start_date = start_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] >= start_date)]
		else:
			
			new_period = node_period
		print(new_period)
		# To display dataframe
		table_content = new_period.to_html()
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
		context = {
			'chart':chart,
			'table_content': table_content,
		}
		return render(request, '../templates/msiapp_templates/customer_energy_price.html', context)
	else:
		customers = ''

		context = {
			'form': customers,
		}
		return render(request, '../templates/msiapp_templates/customer_energy_price.html', context)


@login_required(login_url="login")
def customer_energy_usage_report(request):
	if request.method == 'POST':
		node_name = float(request.POST.get('node_name'))
		start_date = request.POST.get('start_date')
		end_date = request.POST.get('end_date')

		engine = create_engine('mysql+mysqlconnector://Quinn:Holland$1@neura.dyndns.org:3306/NeuraData')
		# period = pd.read_sql("SELECT * FROM vsumperiodvaluesday", engine)
		period = pd.read_sql("SELECT * FROM NeuraData.vsumperiodvaluesdayEnergy", engine)
		node_period = period[(period['Node'] == node_name)]
		#'''
		if start_date == '' and end_date != '':

			# Change date for MySQL
			if end_date:
				end_date = end_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] <= end_date)]

		elif start_date != '' and end_date != '':
			# Change date for MySQL
			if start_date:
				start_date = start_date.replace('-','/')
			# Change date for MySQL
			if end_date:
				end_date = end_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] >= start_date) & (node_period['DateOnly'] <= end_date)]
		elif end_date == '' and start_date != '':
			print('if_3')
			# Change date for MySQL
			start_date = start_date.replace('-','/')
			new_period = node_period[(node_period['DateOnly'] >= start_date)]
		else:
			
			new_period = node_period
		print(new_period)
		# To display dataframe
		table_content = new_period.to_html()
		df = pd.DataFrame(new_period, columns=['DateOnly','Energy'])
		x = []
		y = []
		for column in df:
			columnSeriesObj = df[column]
			if column == 'DateOnly':
				x = columnSeriesObj.values
			elif column == 'Energy':
				y = columnSeriesObj.values
		chart = get_usage_plot(x, y)
		df.plot(x ='DateOnly', y='Energy', kind = 'line')
		context = {
			'chart':chart,
			'table_content': table_content,
		}
		return render(request, '../templates/msiapp_templates/customer_energy_usage.html', context)
	else:
		customers = ''

		context = {
			'form': customers,
		}
		return render(request, '../templates/msiapp_templates/customer_energy_usage.html', context)


@login_required(login_url="login")
def customer_list_device_by_customer(request, pk):
	user = pk
	try:
		customer = Customer.objects.get(user=user)
	# 	print(customer)
	except:
		messages.error(request, 'No Device Present. Please Add New Device')
		return redirect('device')
	device = Device.objects.filter(customers=customer)
	check = len(device)

	if check == 0:
		messages.warning(request, 'No Devices Linked To Customer. Please Add Device')
		return redirect('device')

	my_filter = DeviceFilter(request.GET, queryset=device)
	meetings = my_filter.qs
	context = {
        'myFilter': my_filter,
        'form': meetings,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_list_by_customer.html', context)


@login_required(login_url="login")
def customer_list_customer_by_device(request, pk):
	customers = []
	print(pk)
	try:
		devices = Device.objects.filter(name=pk)
		print(len(devices))
	except:
		messages.warning(request, 'No Device Present. Please Create Device')
		return redirect('device')

	#my_filter = Device(request.GET, queryset=devices)
	# meetings = devices.qs

	context = {
        'myFilter': devices,
        'form': devices,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_list_customer_by_device.html', context)
