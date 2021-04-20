from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def firstpage(request):
	return render(request, "users/firstpage.html")

def user_login(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method=="POST":
		user_name=request.POST.get('username', '')
		user_password=request.POST.get('password', '')
		user=authenticate(username=user_name, password=user_password)
		if user:
			if user.last_login == None:
				login(request, user)
				messages.success(request, "Logged In")
				return redirect("account/creation")
			else:
				login(request, user)
				messages.success(request, "Logged In")
				return redirect("home")
		else:
			messages.error(request, "Invalid Credentials")
			return redirect("login")

	return render(request, 'users/login.html')

def user_logout(request):
	logout(request)
	return redirect("/")

def user_signup(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method=="POST":
		mail=request.POST.get('email', '')
		first_name=request.POST.get('firstname', '')
		last_name=request.POST.get('lastname', '')
		username=request.POST.get('username', '')
		password=request.POST.get('password', '')
		confirmpassword=request.POST.get('confirmpassword', '')
		userCheck=User.objects.filter(username=username) | User.objects.filter(email=mail)
		if userCheck:
			messages.error(request, "Username or email already exists")
			return redirect("signup")
		else:
			if password==confirmpassword:
				user_obj=User.objects.create_user(first_name=first_name, last_name=last_name, password=password, email=mail, username=username)
				user_obj.save()
				messages.success(request, "Signed Up successfully")
				return redirect("login")
			else:
				messages.error(request, "Passwords do not match")

				context={
					'email': mail,
					'firstname': first_name,
					'lastname': last_name,
					'username': username,
				}
				return render(request, 'users/signup.html', context)	
	return render(request, 'users/signup.html')
