from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	userImage=models.ImageField(upload_to="images/", default="images/default.png", null=True, blank=True)
	email=models.CharField(max_length=200)
	contact=models.CharField(max_length=200, blank=True)
	githubprofile=models.URLField(null=True, blank=True)
	bio=models.TextField(blank=True)
	reputation_points=models.IntegerField(default=0)

	def __str__(self):
		return str(self.user)

class Skill(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	skill_value=models.CharField(max_length=200)

	def __str__(self):
		return str(self.user)

class Experience(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	title=models.CharField(max_length=300)
	description=models.TextField(null=True)
	startdate=models.DateField()
	enddate=models.DateField()
	
	def __str__(self):
		return str(self.user)+" "+str(self.title)

