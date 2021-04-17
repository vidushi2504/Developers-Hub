from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Account, Skill, Experience
from home.models import Post
from django.contrib.auth.models import User
from django.views.generic import View
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
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
		messages.success(request, "Account created successfully!")
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
		messages.success(request, "Details edited successfully!")
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

@login_required
def delete_experience(request, exp_id):

	try:
		obj=Experience.objects.filter(id=exp_id)
		obj.delete()
		messages.success(request, "Experience deleted successfully!")
	except:
		messages.warning(request, "Something went wrong. Please try again!")
	return redirect(request.META.get('HTTP_REFERER'))

@login_required
def edit_experience(request, exp_id):

	try:
		obj=Experience.objects.filter(id=exp_id)[0]
		title=request.POST.get('title')
		description=request.POST.get('description')
		obj.title=title
		obj.description=description
		print(title)
		print(description)
		obj.save()
		messages.success(request, "Experience edited successfully!")
	except:
		messages.warning(request, "Something went wrong. Please try again!")
	return redirect(request.META.get('HTTP_REFERER'))

@login_required
def send_message(request, acc_id):

	try:
		account=Account.objects.filter(id=acc_id)[0]
		body=request.POST.get('message', '')
		send_mail(
			"Message from "+account.user.username+" via Developer's Hub",
			body+'You can contact me via email: '+request.user.email,
			'info.developershub@gmail.com',
			[account.email],
			fail_silently=False)
		messages.success(request, "Message sent successfully!")
	except:
		messages.warning(request, "Something went wrong. Please try again!")
	return redirect(request.META.get('HTTP_REFERER'))
