from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account, Skill, Experience
from django.contrib.auth.models import User
from django.views.generic import View

# Create your views here.
def user_account(request, userid):

	user=User.objects.filter(pk=userid).first()
	context={}
	if user:
		details=Account.objects.filter(user=user).first()
		skills=Skill.objects.filter(user=user)
		experiences=Experience.objects.filter(user=user)
		context={
			'details': details,
			'skills': skills,
			'experiences': experiences
		}
	else:
		return HttpResponse("No Such User")

	return render(request, "account/account.html", context)

def user_creation(request):				# change to class based view

	if request.method == "POST":
		mail=request.POST.get('email', '')
		contact=request.POST.get('contact', '')
		skills=request.POST.get('skills', '')
		githubprofile=request.POST.get('github', '')
		bio=request.POST.get('bio', '')
		user=request.user
		obj=Account(user=user, email=mail, contact=contact, githubprofile=githubprofile, bio=bio)
		obj.save()
		skills=skills.split(',')
		for i in skills:
			skill_obj=Skill(user=user, skill_value=i)
			skill_obj.save()
		return redirect('home')

	return render(request, "account/creation.html")

def edit_details(request):

	user=User.objects.filter(pk=request.user.id).first()
	details=Account.objects.filter(user=user).first()
	skillset=Skill.objects.filter(user=user)
	skills=""
	for i in skillset:
		skills+=str(i.skill_value)
		skills+=", "
	skills=skills[:len(skills)-2]
	if request.method=="POST":
		image=request.POST.get('image', )
		first_name=request.POST.get('first_name', '')
		last_name=request.POST.get('last_name', '')
		mail=request.POST.get('email', '')
		contact=request.POST.get('contact', '')
		skills=request.POST.get('skills', '')
		githubprofile=request.POST.get('github', '')
		bio=request.POST.get('bio', '')
		user=request.user
		user_obj=User(first_name=first_name, last_name=last_name)
		obj=Account(user=user, userImage=image, email=mail, contact=contact, githubprofile=githubprofile, bio=bio)
		obj.save()
		skills=skills.split(',')
		for i in skills:
			skill_obj=Skill(user=user, skill_value=i)
			skill_obj.save()
		return redirect('account', request.user.id)

	context = {
		'userobj':user,
		'details':details,
		'skills':skills
	}

	return render(request, "account/editdetails.html", context)