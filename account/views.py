from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account, Skill, Experience
from home.models import Post
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
		image=request.FILES['image'] if 'image' in request.FILES else False
		first_name=request.POST.get('first_name', '')
		last_name=request.POST.get('last_name', '')
		mail=request.POST.get('email', '')
		contact=request.POST.get('contact', '')
		skills=request.POST.get('skills', '')
		githubprofile=request.POST.get('github', '')
		bio=request.POST.get('bio', '')
		user=request.user
		user.first_name=first_name
		user.last_name=last_name
		user.save()

		details.user=user
		if image is not False:
			details.userImage=image
		details.email=mail
		details.contact=contact
		details.githubprofile=githubprofile
		details.bio=bio
		details.save()
		skills=skills.split(',')
		skill_obj=Skill.objects.filter(user=user)
		for i in skills:
			if i not in skill_obj:
				obj=Skill(user=user, skill_value=i)
				obj.save()
		for i in skill_obj:
			if i not in skills:
				i.delete()
		return redirect('account', request.user.id)

	context = {
		'userobj':user,
		'details':details,
		'skills':skills
	}

	return render(request, "account/editdetails.html", context)

def view_posts(request, userid):
	user=User.objects.get(id=userid)
	posts=Post.objects.filter(author=user)
	context={
		'posts':posts
	}
	return render(request, "account/viewpost.html", context)