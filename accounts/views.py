from django.shortcuts import render, redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from contacts.models import Contact


def register(request):
	if request.method=='POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']
		
		if password == password2:
			#check user name
			if User.objects.filter(username=username).exists():
				messages.error(request,'That username is taken')
				return redirect('register')
			else:
				#check user email
				if User.objects.filter(email=email).exists():
					messages.error(request,'That username is taken')
					return redirect('register')
				else:
					#Register User
					user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password,email=email)
					user.save()
					return redirect('dashboard')

		else:
			messages.error(request,'Password not matched')
			return redirect('register')
	else:
		return render(request,'account/register.html')

def login(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(request, username=username, password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('index')
		else:
			messages.error(request,'password or username is not matched')
			return redirect('login')
		
		
	else:
		return render(request,'account/login.html')

def dashboard(request):
	user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
	context = {
		'contacts':user_contacts
	}
	return render(request,'account/dashboard.html',context)

def logout(request):
	if request.method== 'POST':
		auth.logout(request)
		return redirect('index')